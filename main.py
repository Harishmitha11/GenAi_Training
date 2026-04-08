import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from dotenv import load_dotenv

from src.transform import transform_data
from src.audit_logger import ETLAuditTrail

# Load environment variables
load_dotenv()

app = FastAPI(title="LLM-Orchestrated ETL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint for ETL execution
@app.post("/api/etl/run")
async def run_pipeline():
    audit = ETLAuditTrail()
    
    try:
        # Use default dataset
        data_to_process = "data/raw_dataset.csv"
        audit.log_step("Initialize", "Success", {"info": "Using default dataset: data/raw_dataset.csv"})
            
        # Transform
        clean_df = transform_data(data_to_process, audit)
        
        # Load
        db_path = "data/etl_database.db"
        conn = sqlite3.connect(db_path)
        clean_df.to_sql("clean_users", conn, if_exists="replace", index=False)
        audit.metrics["output_rows"] = len(clean_df)
        audit.log_step("Load", "Success", {"target": "SQLite:clean_users", "rows": len(clean_df)})
            
        job_counts = clean_df['job_title'].value_counts().to_dict()
        bins = [-1, 20, 30, 40, 50, 100]
        labels = ['<20', '21-30', '31-40', '41-50', '50+']
        age_bins = pd.cut(pd.to_numeric(clean_df['age'], errors='coerce').fillna(0), bins=bins, labels=labels)
        age_dist = {str(k): int(v) for k, v in age_bins.value_counts().to_dict().items()}

        return JSONResponse(content={
            "status": "success",
            "message": "Pipeline completed successfully",
            "report": audit.generate_report(),
            "visualizations": {
                "departments": {str(k): int(v) for k, v in job_counts.items()},
                "ages": age_dist
            }
        })
        
    except Exception as e:
        audit.log_step("Pipeline_Error", "Fail", {"error": str(e)})
        return JSONResponse(status_code=500, content={
            "status": "error",
            "error": "Pipeline failed", 
            "message": str(e),
            "audit": audit.logs
        })

# Mount static files to serve the frontend UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
