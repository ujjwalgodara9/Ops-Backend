from fastapi import APIRouter, HTTPException
from app.models.schemas import CompareTrustRequest, TrustComparisonResponse
from app.services.trust_comparision_service import compare_trust_responses
from app.services.trust_service import process_trust_document
from app.utils.helpers import base64_to_file
from app.core.logging import logger

router = APIRouter()

@router.post("/compare_trust_documents/", response_model=TrustComparisonResponse)
async def compare_trust_documents(request: CompareTrustRequest):
    try:
        if len(request.captures) != 2:
            raise HTTPException(
                status_code=400,
                detail="Exactly two documents are required for trust comparison"
            )

        # Process each document
        responses = []
        for idx, capture in enumerate(request.captures):
            try:
                document = base64_to_file(capture.data)
                response = await process_trust_document(document, capture.url)
                responses.append(response)
            except HTTPException as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Document {idx + 1} failed validation: {str(e.detail)}"
                )

        # Compare results
        comparison_result = compare_trust_responses(responses[0], responses[1])
        
        return TrustComparisonResponse(
            response1=responses[0].data,
            response2=responses[1].data,
            comparison_result=comparison_result
        )

    except HTTPException as e:
        logger.error(f"Trust comparison error: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Processing error during trust comparison: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during trust document processing")