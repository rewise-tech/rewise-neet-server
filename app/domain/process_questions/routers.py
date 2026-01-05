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


@router.get("/search", response_model=list[schemas.StageQuestionSearchRead])
def search_questions(
    year: str | None = Query(None),
    source: str | None = Query(None),
    subject: str | None = Query(None),
    chapter: str | None = Query(None),
    reviewed: bool | None = Query(None),
    service: StageQuestionService = Depends(get_stage_question_service),
):
    print(year, source, subject, chapter, reviewed)
    return service.search_questions(
        year=year, source=source, subject=subject, chapter=chapter, reviewed=reviewed
    )


@router.get("/sources", response_model=list[str])
def get_unique_sources(
    service: StageQuestionService = Depends(get_stage_question_service),
):
    return service.get_unique_sources()


@router.get("/subjects", response_model=list[str])
def get_unique_subjects(
    service: StageQuestionService = Depends(get_stage_question_service),
):
    return service.get_unique_subjects()


@router.get("/chapters", response_model=list[str])
def get_unique_chapters(
    subject: str | None = Query(None),
    service: StageQuestionService = Depends(get_stage_question_service),
):
    return service.get_unique_chapters(subject=subject)


@router.get("/years", response_model=list[str])
def get_unique_years(
    service: StageQuestionService = Depends(get_stage_question_service),
):
    return service.get_unique_years()


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
