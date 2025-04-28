from fastapi import APIRouter

from app.api.routes import login, problems, users

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(problems.router)
api_router.include_router(users.router)