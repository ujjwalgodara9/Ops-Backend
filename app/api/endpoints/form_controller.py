# app/api/endpoints/form_controller.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import FormExtractionRequest, FormFields
from app.services.form_service import extract_form_data

router = APIRouter()

@router.post("/extract-form", response_model=FormFields)
async def extract_form(data: FormExtractionRequest):
    """
    Extract form fields from an image.
    
    Args:
        data: Request with base64 encoded image
        
    Returns:
        FormFields: Extracted form data
    """
    try:
        return await extract_form_data(data.image)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}