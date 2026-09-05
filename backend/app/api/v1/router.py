from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    projects,
    requirements,
    test_cases,
    ai,
    test_runs,
    dashboard,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(requirements.router)
api_router.include_router(test_cases.router)
api_router.include_router(ai.router)
api_router.include_router(test_runs.router)
api_router.include_router(dashboard.router)
