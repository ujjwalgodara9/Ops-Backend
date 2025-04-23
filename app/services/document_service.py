# app/services/document_service.py
from app.models.schemas import ProcessedResponse, LLM_OPTIONS
from app.services.llm_service import process_image_with_llm, create_prompt
from app.mappings.field_mappings import MAPPINGS_BY_TYPE
from app.core.logging import logger
from fastapi import HTTPException
import PIL.Image

async def process_image(image: PIL.Image.Image, url: str, image_number: int, llm: LLM_OPTIONS = "gemini") -> ProcessedResponse:
    """
    Process a single image with LLM using mapping determined by URL.
    
    Args:
        image: PIL.Image.Image object to process
        url: URL string containing image identifier
        image_number: Sequential number (1, 2, or 3) for logging purposes
        llm: Which LLM to use (gemini or openai)
    
    Returns:
        ProcessedResponse: Extracted data and document type
    """
    # Determine mapping and document type from URL
    mapping = None
    document_type = None

    for bank_type, bank_mapping in MAPPINGS_BY_TYPE.items():
        if bank_type.lower() in url.lower():
            mapping = bank_mapping
            document_type = bank_type
            break

    if not mapping:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to determine document type from URL for image {image_number}. Valid types: desna, tna1, auspaynet"
        )

    # Create prompt for LLM processing
    prompt = create_prompt(mapping)
    
    # Process image with LLM
    try:
        extracted_data = await process_image_with_llm(image, mapping, prompt, llm)
        
        return ProcessedResponse(
            data=extracted_data,
            document_type=document_type
        )
    except Exception as e:
        logger.error(f"Error processing image {image_number}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image {image_number}: {str(e)}")