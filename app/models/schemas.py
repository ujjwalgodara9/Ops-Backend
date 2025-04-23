# app/models/schemas.py
from pydantic import BaseModel
from typing import Dict, List, Optional, Literal

LLM_OPTIONS = Literal["gemini", "openai"]

class CaptureData(BaseModel):
    data: str
    url: str

class CompareRequest(BaseModel):
    captures: List[CaptureData]  # List of base64-encoded images

class ProcessedResponse(BaseModel):
    data: Dict
    document_type: str

class ComparisonResponse(BaseModel):
    response1: dict
    response2: dict
    response3: dict
    comparison_result: dict

class FormExtractionRequest(BaseModel):
    image: str  # Base64 encoded image string

class FormFields(BaseModel):
    user_name: Optional[str] = None
    user_id: Optional[str] = None
    bureau_name: Optional[str] = None
    amt_limit_in_figures: Optional[str] = None
    amt_limit_in_words: Optional[str] = None
    limit_frequency: Optional[str] = None
    period_ending: Optional[str] = None
    drawing_account_name: Optional[str] = None
    bsb: Optional[str] = None
    account_number: Optional[str] = None
    temporary_processing_limit_override: Optional[str] = None