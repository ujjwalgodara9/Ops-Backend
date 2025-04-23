# app/services/form_service.py
import json
import base64
import io
import PIL.Image
from app.services.llm_service import gemini_model, create_form_prompt
from app.mappings.field_mappings import MAPPING_IMG1
from app.models.schemas import FormFields
from app.utils.helpers import clean_base64
from fastapi import HTTPException

async def extract_form_data(image_data: str) -> FormFields:
    """
    Extract form data from an image.
    
    Args:
        image_data: Base64 encoded image string
        
    Returns:
        FormFields: Extracted form data
    """
    try:
        # Clean and decode base64
        cleaned_base64 = clean_base64(image_data)
        image_bytes = base64.b64decode(cleaned_base64)
        
        # Verify image validity
        image = PIL.Image.open(io.BytesIO(image_bytes))
        image.verify()  # Check if image is valid
        
        # Reopen for actual processing
        image = PIL.Image.open(io.BytesIO(image_bytes))

        # Create structured prompt
        prompt = create_form_prompt(MAPPING_IMG1)

        # Generate response
        response = gemini_model.generate_content([prompt, image])
        
        # Extract JSON from response
        response_text = response.text.strip()
        json_str = response_text.split("{", 1)[-1].rsplit("}", 1)[0]
        json_str = "{" + json_str + "}"
        
        extracted_data = json.loads(json_str)
        return FormFields(**extracted_data)

    except (base64.binascii.Error, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, 
                          detail=f"Failed to parse Gemini response: {str(e)}. Response was: {response_text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))