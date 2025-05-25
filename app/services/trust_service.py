from typing import Union
import re
from datetime import datetime
import json
import os
import PIL.Image
from fastapi import HTTPException
from app.core.logging import logger
from app.mappings.field_mappings import TRUST_MAPPINGS_BY_TYPE, GLOBAL_TRUST_MAPPING
from app.models.schemas import TrustInfo, ProcessedTrustResponse
from app.services.llm_service import process_pdf_with_llm, process_image_with_llm

# def create_trust_prompt(mapping: dict) -> str:
#     """Create a prompt for trust document processing"""
#     return f"""
#     Extract trust information from this document using these exact field mappings:
#     {json.dumps(mapping, indent=2)}
    
#     Rules:
#     1. Return valid JSON ONLY with these exact field names: {list(GLOBAL_TRUST_MAPPING.keys())}
#     2. Normalize data:
#        - Dates: Convert to DD/MM/YYYY format (handle formats like '23rd June 2016')
#        - Names: Remove titles (Mr/Mrs) and normalize case
#        - Addresses: Combine multi-line with newlines
#        - Amounts: Remove currency symbols, keep only numbers
#     3. For arrays (trustees, beneficiaries):
#        - Split by 'and', commas, or newlines
#        - Return as lists even if single item
#     4. For unit holders:
#        - Format as [{{"name": "...", "units": number}}]
#        - Convert units to integers
#     5. Return null for missing fields
#     6. For required fields (all except unit_holders), make best effort to extract
#     """

def create_trust_prompt(mapping: dict) -> str:
    """Create a more detailed prompt for trust document processing"""
    return f"""
    Carefully analyze this trust document and extract the following information:

    REQUIRED FIELDS (must extract all):
    1. Trust Type: {mapping.get('trust_type')} -> 'trust_type'
    2. Trustees: {mapping.get('trustees')} -> 'trustees' (array)
    3. Trustee Address: {mapping.get('trustee_address')} -> 'trustee_address'
    4. Beneficiaries: {mapping.get('beneficiaries')} -> 'beneficiaries' (array)
    5. Date Executed: {mapping.get('date_executed')} -> 'date_executed' (DD/MM/YYYY)
    6. Settled Sum: {mapping.get('settled_sum')} -> 'settled_sum' (number only)
    7. Governing State: {mapping.get('governing_state')} -> 'governing_state'

    OPTIONAL FIELD:
    - Unit Holders: {mapping.get('unit_holders')} -> 'unit_holders' (array of {{name, units}})

    IMPORTANT RULES:
    1. For missing required fields, make your best guess from context
    2. For dates: Convert formats like '23rd June 2016' to '23/06/2016'
    3. For names: Remove titles (Mr/Mrs) and normalize formatting
    4. For amounts: Extract only numbers (no '$' or words)
    5. For addresses: Preserve line breaks as '\\n'

    Return ONLY valid JSON with these exact field names:
    {list(GLOBAL_TRUST_MAPPING.keys())}

    Example Output:
    {{
        "trust_type": "Family Trust",
        "trustees": ["John Smith", "Jane Smith"],
        "trustee_address": "123 Main St\\nSydney",
        "beneficiaries": ["Alice Smith", "Bob Smith"],
        "date_executed": "01/01/2020",
        "settled_sum": "100",
        "governing_state": "NSW",
        "unit_holders": [{{"name": "John Smith", "units": 50}}]
    }}
    """
    
async def process_trust_document(content: Union[PIL.Image.Image, str], url: str) -> ProcessedTrustResponse:
    """Process trust document with better error handling"""
    try:
        # Determine document type from URL
        doc_type = None
        url_lower = url.lower()
        
        if "online" in url_lower:
            doc_type = "online"
        elif "schedule" in url_lower:
            doc_type = "schedule"
        
        if not doc_type:
            raise HTTPException(
                status_code=400,
                detail="URL must contain 'online' or 'schedule' to identify document type"
            )
        
        # Get the appropriate mapping
        mapping = TRUST_MAPPINGS_BY_TYPE[doc_type]
        prompt = create_trust_prompt(mapping)
        
        # Process document based on content type
        try:
            if isinstance(content, str) and content.endswith('.pdf'):  # PDF file path
                extracted_data = await process_pdf_with_llm(content, prompt, "gemini")
            else:  # Image
                extracted_data = await process_image_with_llm(content, prompt, "gemini")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Document processing failed: {str(e)}"
            )
        
        # Post-processing validation
        required_fields = {
            'trust_type': str,
            'trustees': list,
            'trustee_address': str,
            'beneficiaries': list,
            'date_executed': str,
            'settled_sum': str,
            'governing_state': str
        }
        
        missing_fields = []
        for field, field_type in required_fields.items():
            if field not in extracted_data or not extracted_data[field]:
                missing_fields.append(field)
            elif not isinstance(extracted_data[field], field_type):
                try:
                    # Try to convert to correct type
                    if field_type == list:
                        extracted_data[field] = [extracted_data[field]]
                    else:
                        extracted_data[field] = str(extracted_data[field])
                except:
                    missing_fields.append(field)
        
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing or invalid required fields: {', '.join(missing_fields)}"
            )
        
        return ProcessedTrustResponse(
            data=TrustInfo(**extracted_data)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing trust document: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Trust document processing failed: {str(e)}"
        )
    finally:
        if isinstance(content, str) and os.path.exists(content):
            try:
                os.unlink(content)
            except:
                pass