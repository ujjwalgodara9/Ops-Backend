# app/api/endpoints/document_controller.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import CompareRequest, ComparisonResponse
from app.services.document_service import process_image
from app.services.comparison_service import compare_responses
from app.utils.helpers import base64_to_file, base64_to_image
from app.core.logging import logger
from datetime import datetime
import asyncio

router = APIRouter()

# app/api/endpoints/document_controller.py
@router.post("/compare_documents/", response_model=ComparisonResponse)
async def compare_documents(request: CompareRequest):
    try:
        if len(request.captures) != 3:
            raise HTTPException(
                status_code=400,
                detail="Exactly three documents are required for comparison. "
                       "Expected formats: 'auspaynet tna.pdf', 'desna.pdf', or 'tna.pdf'"
            )

        # Process each document with strict URL checking
        responses = []
        for idx, capture in enumerate(request.captures):
            try:
                document = base64_to_file(capture.data)
                response = await process_image(document, capture.url, idx + 1)
                responses.append(response)
            except HTTPException as e:
                # Add which document failed in the error message
                raise HTTPException(
                    status_code=400,
                    detail=f"Document {idx + 1} failed validation: {str(e.detail)}"
                )

        comparison_result = compare_responses(responses)
        
        return ComparisonResponse(
            response1=responses[0].data,
            response2=responses[1].data,
            response3=responses[2].data,
            comparison_result=comparison_result
        )

    except HTTPException as e:
        logger.error(f"Validation error: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during document processing")