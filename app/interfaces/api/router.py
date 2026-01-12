from fastapi import APIRouter

from app.domain.questions.routers import router as questions_router
from app.domain.users.routers import router as users_router
from app.domain.process_questions.routers import router as process_questions_router
from app.domain.subjects.routers import router as subjects_router
from app.domain.test.routers import router as test_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(questions_router)
api_router.include_router(process_questions_router)
api_router.include_router(subjects_router)
api_router.include_router(test_router)
