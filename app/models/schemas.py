# app/models/schemas.py
from pydantic import BaseModel
from typing import Dict, List, Optional, Literal

LLM_OPTIONS = Literal["gemini", "openai"]

class CaptureData(BaseModel):
    data: str
    url: str

class CompareRequest(BaseModel):
    captures: List[CaptureData]  # List of base64-encoded images

class CompareTrustRequest(BaseModel):
    captures: List[CaptureData]  
    
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
    
class TrustInfo(BaseModel):
    type_of_trust: Optional[str] = None
    trustees: List[str] = []
    trustee_address: Optional[str] = None
    beneficiaries: List[str] = []
    beneficiary_addresses: List[str] = []
    abn: Optional[str] = None
    date_executed: Optional[str] = None
    settlor_name: Optional[str] = None
    settled_sum: Optional[str] = None
    governing_state: Optional[str] = None
    unit_holders: List[dict] = []  # {name: str, units: int}

class ProcessedTrustResponse(BaseModel):
    data: TrustInfo

class TrustComparisonResponse(BaseModel):
    response1: TrustInfo
    response2: TrustInfo
    comparison_result: dict