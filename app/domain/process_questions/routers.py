from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.process_questions import schemas
from app.domain.process_questions.services import StageQuestionService

router = APIRouter(prefix="/process-questions", tags=["process-questions"])


def get_stage_question_service(db: Session = Depends(get_db)) -> StageQuestionService:
    return StageQuestionService(db)


@router.get("/", response_model=list[schemas.StageQuestionRead])
def list_questions(service: StageQuestionService = Depends(get_stage_question_service)):
    return service.list_questions()


@router.get("/search", response_model=list[schemas.StageQuestionYearSearchRead])
def search_questions_by_year(
    year: str = Query(...),
    service: StageQuestionService = Depends(get_stage_question_service),
):
    return service.search_questions_by_year(year)


@router.get(
    "/by-question-number/{question_number}", response_model=schemas.StageQuestionRead
)
def get_question_by_question_number(
    question_number: str,
    year: str = Query(...),
    service: StageQuestionService = Depends(get_stage_question_service),
):
    question = service.get_question_by_question_number(
        year=year, question_number=question_number
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="StageQuestion not found"
        )
    return question


@router.get("/{question_id}", response_model=schemas.StageQuestionRead)
def get_question(
    question_id: int,
    service: StageQuestionService = Depends(get_stage_question_service),
):
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="StageQuestion not found"
        )
    return question


@router.post(
    "/", response_model=schemas.StageQuestionRead, status_code=status.HTTP_201_CREATED
)
def create_question(
    payload: schemas.StageQuestionCreate,
    service: StageQuestionService = Depends(get_stage_question_service),
):
    return service.create_question(payload)


@router.patch("/{question_id}", response_model=schemas.StageQuestionRead)
def update_question(
    question_id: int,
    payload: schemas.StageQuestionUpdate,
    service: StageQuestionService = Depends(get_stage_question_service),
):
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="StageQuestion not found"
        )
    return service.update_question(question, payload)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: int,
    service: StageQuestionService = Depends(get_stage_question_service),
):
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="StageQuestion not found"
        )
    service.delete_question(question)
