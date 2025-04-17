from fastapi import APIRouter

from app.api.routes import problems, users

api_router = APIRouter()
api_router.include_router(problems.router)
api_router.include_router(users.router)