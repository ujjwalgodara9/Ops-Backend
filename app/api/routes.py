# app/api/routes.py
from fastapi import APIRouter
from app.api.endpoints import document_controller, form_controller

api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(document_controller.router, tags=["Documents"])
api_router.include_router(form_controller.router, tags=["Forms"])