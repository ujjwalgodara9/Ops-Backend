# app/services/llm_service.py
import google.generativeai as genai
import json
from PIL import Image
from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import LLM_OPTIONS, ProcessedResponse   
from fastapi import HTTPException
import tempfile


# Initialize Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
gemini_model2 = genai.GenerativeModel(settings.GEMINI_MODEL_2)

async def process_image_with_llm(image: Image.Image, mapping: dict, prompt: str, llm: LLM_OPTIONS = "gemini") -> dict:
    """
    Process an image using the specified LLM (Gemini by default)
    
    Args:
        image: PIL.Image object
        mapping: Dictionary mapping for the document
        prompt: The prompt for the LLM
        llm: Which LLM to use (gemini or openai)
        
    Returns:
        dict: Extracted data from the image
    """
    try:
        if llm == "gemini":
            response = gemini_model.generate_content(
                [prompt, image],
                generation_config=genai.GenerationConfig(
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
        elif llm == "openai":
            response = gemini_model2.generate_content(
                [prompt, image],
                generation_config=genai.GenerationConfig(
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
        else:
            raise ValueError(f"Unsupported LLM option: {llm}")
        
        extracted_data = json.loads(response.text)
        
        # Handle response structure
        if isinstance(extracted_data, list):
            extracted_data = extracted_data[0]
            
        # Apply default values for missing fields
        if isinstance(extracted_data, dict):
            if 'period_ending' not in extracted_data:
                extracted_data['period_ending'] = "Until further notice"
            if 'temporary_processing_limit_override' not in extracted_data:
                extracted_data['temporary_processing_limit_override'] = "none"
        
        return extracted_data
        
    except Exception as e:
        logger.error(f"Error processing image with {llm}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image with {llm}: {str(e)}")

def create_prompt(mapping: dict) -> str:
    """
    Create a prompt for image processing based on the mapping
    
    Args:
        mapping: Dictionary mapping for the document
        
    Returns:
        str: The prompt for the LLM
    """
    return f"""
    Extract information from this image using the following guidelines:
    
    1. Extract values for all visible fields and map them according to these rules: {mapping}
    2. For amount fields:
       - Remove any currency symbols or commas
       - Keep only the numeric value for figures
       - Keep only the words for word amounts
    3. For dates:
       - Return in DD/MM/YYYY format
    4. For period_ending:
       - If not explicitly mentioned, return "Until further notice"
    5. For temporary_processing_limit_override:
       - If not mentioned, return "none"
    6. For limit_frequency:
       - Return only the selected/ticked option
    
    Format the output as a strict JSON object with the mapped field names as keys.
    Remove any prefixes, suffixes, or additional text from the extracted values.
    Ensure all values are strings.
    """

def create_form_prompt(mapping: dict) -> str:
    """
    Create a prompt for form extraction
    
    Args:
        mapping: Dictionary mapping for the form
        
    Returns:
        str: The prompt for the LLM
    """
    return f"""Analyze this financial document image and extract these fields:
    {json.dumps({v: f"from '{k}'" for k, v in mapping.items()}, indent=4)}

    Rules:
    1. Return valid JSON ONLY
    2. Use field names: {list(mapping.values())}
    3. Preserve original formatting
    4. Return null for missing fields
    5. Handle dates as strings in original format
    6. Currency values should include symbols
    7. Same exact field names might not be present but contextually they can be same

    JSON Output:"""
    

async def process_pdf_with_llm(pdf_path: str, mapping: dict, prompt: str, llm: LLM_OPTIONS = "gemini") -> dict:
    """
    Process a PDF file using the specified LLM
    
    Args:
        pdf_path: Path to PDF file
        mapping: Dictionary mapping for the document
        prompt: The prompt for the LLM
        llm: Which LLM to use (gemini or openai)
        
    Returns:
        dict: Extracted data from the PDF
    """
    try:
        if llm == "gemini":
            model = gemini_model
        elif llm == "openai":
            model = gemini_model2
        else:
            raise ValueError(f"Unsupported LLM option: {llm}")
        
        # Read PDF as bytes
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        
        # Generate content with the PDF
        response = model.generate_content(
            [prompt, {"mime_type": "application/pdf", "data": pdf_bytes}],
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                response_mime_type="application/json"
            )
        )
        
        
        extracted_data = json.loads(response.text)
        
        # Handle response structure
        if isinstance(extracted_data, list):
            extracted_data = extracted_data[0]
            
        # Apply default values for missing fields
        if isinstance(extracted_data, dict):
            if 'period_ending' not in extracted_data:
                extracted_data['period_ending'] = "Until further notice"
            if 'temporary_processing_limit_override' not in extracted_data:
                extracted_data['temporary_processing_limit_override'] = "none"
        
        return extracted_data
        
    except Exception as e:
        logger.error(f"Error processing PDF with {llm}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF with {llm}: {str(e)}")