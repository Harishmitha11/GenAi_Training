import pandas as pd
import json
from langchain_openai import ChatOpenAI
from src.guardrails import SemanticCleaningResponse
from src.audit_logger import ETLAuditTrail

def transform_data(csv_path: str, audit: ETLAuditTrail) -> pd.DataFrame:
    # 1. Extract
    df = pd.read_csv(csv_path)
    audit.metrics["input_rows"] = len(df)
    audit.log_step("Extract", "Success", {"file": csv_path, "rows": len(df)})

    # 2. Transform - Deterministic (Pandas)
    initial_nulls = df['age'].isna().sum() + df['name'].isna().sum() + df['id'].isna().sum()
    df.dropna(subset=['id', 'name'], inplace=True) # Drop missing critical data
    df = df.copy() # Avoid SettingWithCopyWarning
    audit.metrics["nulls_handled"] = int(initial_nulls)
    audit.log_step("Transform_Deterministic", "Success", {"action": "Dropped rows with null primary keys", "rows_remaining": len(df)})

    import os
    
    # 3. Transform - Semantic (LangChain or Mock)
    api_key = os.environ.get("OPENAI_API_KEY")
    is_mock = not api_key or api_key.strip() == "" or api_key == "your_openai_api_key_here"
    
    messy_data = df[['id', 'email', 'job_title', 'age']].to_dict(orient="records")
    audit.log_step("Transform_Semantic_Start", "Pending", {"records_to_process": len(messy_data), "mode": "Mock" if is_mock else "GPT-4o-mini"})
    
    try:
        if is_mock:
            # Mock behavior wrapped in a LangChain runnable to ensure it traces to LangSmith
            from langchain_core.runnables import chain
            
            @chain
            def run_mock_cleaning(data):
                import time
                time.sleep(1.5) # simulate network
                from src.guardrails import CleanedRecord
                mock_recs = []
                for r in data:
                    title = r.get('job_title', '')
                    if 'Sales' in str(title): clean_title = 'Sales'
                    elif 'Dev' in str(title) or 'Data' in str(title): clean_title = 'Engineering'
                    elif 'marketing' in str(title).lower(): clean_title = 'Marketing'
                    elif 'CTO' in str(title): clean_title = 'Executive'
                    else: clean_title = 'Other'
                    
                    age_val = r.get('age')
                    if str(age_val).lower() == 'forty-two': age_val = 42
                    elif str(age_val).lower() == 'twenty-eight': age_val = 28
                    else:
                        try: age_val = int(age_val)
                        except: age_val = 0
                        
                    is_valid = '@' in str(r.get('email', ''))
                    
                    mock_recs.append(CleanedRecord(
                        id=r['id'],
                        standardized_title=clean_title,
                        is_valid_email=is_valid,
                        extracted_age=age_val
                    ))
                return mock_recs
                
            mock_records = run_mock_cleaning.invoke(messy_data)
            
            cleaned_dict = {r.id: r for r in mock_records}
            audit.log_step("Transform_Semantic", "Success", {"records_processed": len(mock_records), "note": "Used Mock Data (No API Key)"})
        else:
            # Actual LangChain behavior
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            structured_llm = llm.with_structured_output(SemanticCleaningResponse)
            
            prompt = f"""
            You are a strict data cleaning assistant. Clean the following records according to the schema.
            Maintain the EXACT order of the records.
            Records to clean: {messy_data}
            """
            
            result = structured_llm.invoke(prompt)
            audit.log_step("Transform_Semantic", "Success", {"records_processed": len(result.records)})
            cleaned_dict = {r.id: r for r in result.records}
        
        df['job_title'] = df['id'].apply(lambda x: cleaned_dict[x].standardized_title if x in cleaned_dict else "Unknown")
        df['is_valid_email'] = df['id'].apply(lambda x: cleaned_dict[x].is_valid_email if x in cleaned_dict else False)
        df['age'] = df['id'].apply(lambda x: cleaned_dict[x].extracted_age if x in cleaned_dict else 0)
        
    except Exception as e:
        audit.log_step("Transform_Semantic", "Failed", {"error": str(e)})
        raise e
        
    return df
