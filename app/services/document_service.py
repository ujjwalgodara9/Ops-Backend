# app/services/document_service.py
import os
from typing import Union
from urllib.parse import unquote, urlparse
from pathlib import Path
from app.models.schemas import ProcessedResponse, LLM_OPTIONS
from app.services.llm_service import process_image_with_llm, process_pdf_with_llm, create_prompt
from app.mappings.field_mappings import MAPPINGS_BY_TYPE
from app.core.logging import logger
from fastapi import HTTPException
import PIL.Image

# app/services/document_service.py
async def process_image(image: Union[PIL.Image.Image, str], url: str, image_number: int, llm: LLM_OPTIONS = "gemini") -> ProcessedResponse:
    """
    Process a single image or PDF with LLM using mapping determined by URL.
    Strict URL checking based on specific patterns.
    """
    
    # # Parse the URL and get the filename
    # Safely parse URL and extract filename
    parsed_url = urlparse(url)
    filename = unquote(parsed_url.path)  # Decode URL-encoded characters
    filename = Path(filename).name.lower()  # Get just the filename

    # Determine mapping and document type from filename
    mapping = None
    document_type = None

    # Strict filename checks
    if "auspaynet" in filename:
        document_type = "auspaynet"
        mapping = MAPPINGS_BY_TYPE["auspaynet"]
    elif "desna" in filename:
        document_type = "desna"
        mapping = MAPPINGS_BY_TYPE["desna"]
    elif "tna" in filename:  # Exact match for tna.pdf
        document_type = "tna1"
        mapping = MAPPINGS_BY_TYPE["tna1"]
    else:
        raise HTTPException(
            status_code=400,
            detail=f"URL filename '{filename}' doesn't match any known document patterns. "
                   f"Expected formats: 'auspaynet tna.pdf', 'desna_Mismatch.pdf', or 'tna.pdf'"
        )

    # Create prompt for LLM processing
    prompt = create_prompt(mapping)
    
    try:
        if isinstance(image, str):  # This is a PDF file path
            extracted_data = await process_pdf_with_llm(image, mapping, prompt, llm)
            # Clean up temporary file
            try:
                os.unlink(image)
            except:
                pass
        else:  # This is a PIL Image
            extracted_data = await process_image_with_llm(image, mapping, prompt, llm)
        
        return ProcessedResponse(
            data=extracted_data,
            document_type=document_type
        )
    except Exception as e:
        logger.error(f"Error processing document {image_number}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document {image_number}: {str(e)}")