from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.questions import schemas
from app.domain.questions.services import QuestionService
from app.domain.process_questions.services import StageQuestionService

router = APIRouter(prefix="/questions", tags=["questions"])


def get_question_service(db: Session = Depends(get_db)) -> QuestionService:
    return QuestionService(db)


def get_stage_question_service(db: Session = Depends(get_db)) -> StageQuestionService:
    return StageQuestionService(db)


@router.get("/", response_model=list[schemas.QuestionRead])
def list_questions(service: QuestionService = Depends(get_question_service)):
    return service.list_questions()


@router.get("/search", response_model=list[schemas.QuestionYearSearchRead])
def search_questions_by_year(
    year: str = Query(...),
    service: QuestionService = Depends(get_question_service),
):
    return service.search_questions_by_year(year)


@router.get(
    "/by-question-number/{question_number}", response_model=schemas.QuestionRead
)
def get_question_by_question_number(
    question_number: str,
    year: str = Query(...),
    service: QuestionService = Depends(get_question_service),
):
    question = service.get_question_by_question_number(
        year=year, question_number=question_number
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    return question


@router.get("/{question_id}", response_model=schemas.QuestionRead)
def get_question(
    question_id: int,
    service: QuestionService = Depends(get_question_service),
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
    question_id: int,
    service: QuestionService = Depends(get_question_service),
):
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    service.delete_question(question)


@router.post(
    "/move_question/{stage_question_id}",
    response_model=schemas.QuestionRead,
    status_code=status.HTTP_201_CREATED,
)
def move_question(
    stage_question_id: int,
    service: QuestionService = Depends(get_question_service),
    stage_service: StageQuestionService = Depends(get_stage_question_service),
):
    stage_question = stage_service.get_question(stage_question_id)
    if not stage_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stage Question not found"
        )

    # Map StageQuestion to QuestionCreate
    options = []
    for opt in stage_question.options:
        options.append(
            schemas.OptionCreate(
                label=opt.label,
                text=opt.text,
                has_diagram=opt.has_diagram,
                diagram_description=opt.diagram_description,
                diagram_name=opt.diagram_name,
            )
        )

    question_create = schemas.QuestionCreate(
        source=stage_question.source,
        year=stage_question.year,
        subject=stage_question.subject,
        chapter=stage_question.chapter,
        topic=stage_question.topic,
        question_number=stage_question.question_number,
        question_text=stage_question.question_text,
        difficulty=stage_question.difficulty,
        has_diagram=stage_question.has_diagram,
        diagram_description=stage_question.diagram_description,
        diagram_position=stage_question.diagram_position,
        diagram_name=stage_question.diagram_name,
        answer=stage_question.answer,
        ai_answer=stage_question.ai_answer,
        solution=stage_question.solution,
        reviewed=stage_question.reviewed,
        options=options,
    )

    return service.create_question(question_create)
