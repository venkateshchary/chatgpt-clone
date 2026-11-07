from fastapi import APIRouter
# from app.api.v1 import user_router
from .conversion_router import router

v1_router = APIRouter()

# Include feature routers here. This acts as the single point of entry for V1.
v1_router.include_router(router)
# v1_router.include_router(user_router)
