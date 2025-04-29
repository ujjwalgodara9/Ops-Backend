# app/api/endpoints/document_controller.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import CompareRequest, ComparisonResponse
from app.services.document_service import process_image
from app.services.comparison_service import compare_responses
from app.utils.helpers import base64_to_image
from app.core.logging import logger
from datetime import datetime
import asyncio

router = APIRouter()

@router.post("/compare_documents/", response_model=ComparisonResponse)
async def compare_documents(request: CompareRequest):
    """
    Endpoint to compare three documents and extract information.
    Accepts three base64-encoded images.
    """
    request_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_context = {'request_id': request_id}

    logger.info("Starting document comparison" )

    try:
        if len(request.captures) != 3:
            raise HTTPException(status_code=400, detail="Exactly three images are required for comparison.")

        logger.info("Converting base64 images to PIL images" )
        images = [base64_to_image(capture.data) for capture in request.captures]

        logger.info("Processing images with Gemini")
        responses = await asyncio.gather(*[
            process_image(img, capture.url, idx + 1)
            for idx, (img, capture) in enumerate(zip(images, request.captures))
        ])

        comparison_result = compare_responses(responses)

        logger.info(
            f"Comparison completed. Status: {comparison_result.get('status', 'Unknown')}"
        )
        
        logger.info("HEhehehehheheh")
        logger.info(ComparisonResponse(
            response1=responses[0].data,
            response2=responses[1].data,
            response3=responses[2].data,
            comparison_result=comparison_result
        ) )

        return ComparisonResponse(
            response1=responses[0].data,
            response2=responses[1].data,
            response3=responses[2].data,
            comparison_result=comparison_result
        )

    except HTTPException as e:
        logger.error(
            f"HTTP error during document comparison: {str(e.detail)}",
            exc_info=True,
            extra=log_context
        )
        raise e
    except Exception as e:
        logger.error(
            f"Error during document comparison: {str(e)}",
            exc_info=True,
            extra=log_context
        )
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare_documents_openai/", response_model=ComparisonResponse)
async def compare_documents_openai(request: CompareRequest):
    """
    Endpoint to compare three documents and extract information using OpenAI.
    Accepts three base64-encoded images.
    """
    request_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_context = {'request_id': request_id}

    logger.info("Starting document comparison with Open API" )

    try:
        if len(request.captures) != 3:
            raise HTTPException(status_code=400, detail="Exactly three images are required for comparison.")

        logger.info("Converting base64 images to PIL images" )
        images = [base64_to_image(capture.data) for capture in request.captures]

        logger.info("Processing images with OPEN API" )
        responses = await asyncio.gather(*[
            process_image(img, capture.url, idx + 1, llm="openai")
            for idx, (img, capture) in enumerate(zip(images, request.captures))
        ])

        comparison_result = compare_responses(responses)

        logger.info(
            f"Comparison completed. Status: {comparison_result.get('status', 'Unknown')}",
            extra=log_context
        )

        return ComparisonResponse(
            response1=responses[0].data,
            response2=responses[1].data,
            response3=responses[2].data,
            comparison_result=comparison_result
        )

    except HTTPException as e:
        logger.error(
            f"HTTP error during document comparison: {str(e.detail)}",
            exc_info=True,
            extra=log_context
        )
        raise e
    except Exception as e:
        logger.error(
            f"Error during document comparison: {str(e)}",
            exc_info=True,
            extra=log_context
        )
        raise HTTPException(status_code=500, detail=str(e))