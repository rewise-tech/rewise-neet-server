from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.questions import schemas
from app.domain.questions.services import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])


def get_question_service(db: Session = Depends(get_db)) -> QuestionService:
    return QuestionService(db)


@router.get("/", response_model=list[schemas.QuestionRead])
def list_questions(service: QuestionService = Depends(get_question_service)):
    return service.list_questions()


@router.get("/{question_id}", response_model=schemas.QuestionRead)
def get_question(
    question_id: int, service: QuestionService = Depends(get_question_service)
):
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    return question


@router.post(
    "/", response_model=schemas.QuestionRead, status_code=status.HTTP_201_CREATED
)
def create_question(
    payload: schemas.QuestionCreate,
    service: QuestionService = Depends(get_question_service),
):
    return service.create_question(payload)


@router.patch("/{question_id}", response_model=schemas.QuestionRead)
def update_question(
    question_id: int,
    payload: schemas.QuestionUpdate,
    service: QuestionService = Depends(get_question_service),
):
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    return service.update_question(question, payload)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: int, service: QuestionService = Depends(get_question_service)
):
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    service.delete_question(question)
