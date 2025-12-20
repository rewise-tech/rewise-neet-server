from fastapi import APIRouter

from app.domain.users.routers import router as users_router

api_router = APIRouter()
api_router.include_router(users_router)
