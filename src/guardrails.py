from pydantic import BaseModel, Field

class CleanedRecord(BaseModel):
    id: int = Field(description="The numeric ID of the user. Very important to keep.")
    standardized_title: str = Field(description="The standardized job category (e.g., 'Engineering', 'Marketing', 'Sales', 'Data', 'HR', 'Executive')")
    is_valid_email: bool = Field(description="True if the email format looks valid, False otherwise.")
    extracted_age: int = Field(description="Numeric age extracted from text, or 0 if missing/invalid.")

class SemanticCleaningResponse(BaseModel):
    records: list[CleanedRecord] = Field(description="List of cleaned semantic records corresponding exactly to the input order")
