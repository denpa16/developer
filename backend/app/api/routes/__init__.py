from fastapi import APIRouter

from .buildings import router as buildings_router
from .projects import router as projects_router

api_router = APIRouter(prefix="/api")
api_router.include_router(projects_router)
api_router.include_router(buildings_router)
