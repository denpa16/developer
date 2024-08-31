from fastapi import APIRouter

from .buildings import router as buildings_router
from .floors import router as floors_router
from .projects import router as projects_router
from .properties import router as properties_router
from .sections import router as sections_router

api_router = APIRouter(prefix="/api")
api_router.include_router(projects_router)
api_router.include_router(buildings_router)
api_router.include_router(sections_router)
api_router.include_router(floors_router)
api_router.include_router(properties_router)
