from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.test import schemas
from app.domain.test.services import TestSettingsService, TestService, MockTestService

from app.domain.questions.schemas import QuestionRead

router = APIRouter(prefix="/test", tags=["test"])


def get_test_settings_service(db: Session = Depends(get_db)) -> TestSettingsService:
    return TestSettingsService(db)


def get_test_service(db: Session = Depends(get_db)) -> TestService:
    return TestService(db)


def get_mock_test_service(db: Session = Depends(get_db)) -> MockTestService:
    return MockTestService(db)


@router.get("/prepare", response_model=list[QuestionRead])
def prepare_test(
    service: TestService = Depends(get_test_service),
):
    return service.prepare_test()


@router.get("/questions/{subject_name}", response_model=list[QuestionRead])
def get_questions_by_subject(
    subject_name: str,
    service: TestService = Depends(get_test_service),
):
    return service.get_questions_by_subject(subject_name)


@router.get("/settings", response_model=list[schemas.TestSettingsRead])
def list_settings(service: TestSettingsService = Depends(get_test_settings_service)):
    return service.list_settings()


@router.get("/settings/{settings_id}", response_model=schemas.TestSettingsRead)
def get_settings(
    settings_id: int,
    service: TestSettingsService = Depends(get_test_settings_service),
):
    settings = service.get_settings(settings_id)
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found"
        )
    return settings


@router.get("/settings/by-key/{key}", response_model=schemas.TestSettingsRead)
def get_settings_by_key(
    key: str,
    service: TestSettingsService = Depends(get_test_settings_service),
):
    settings = service.get_settings_by_key(key)
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found"
        )
    return settings


@router.post(
    "/settings",
    response_model=schemas.TestSettingsRead,
    status_code=status.HTTP_201_CREATED,
)
def create_settings(
    payload: schemas.TestSettingsCreate,
    service: TestSettingsService = Depends(get_test_settings_service),
):
    return service.create_settings(payload)


@router.patch("/settings/{settings_id}", response_model=schemas.TestSettingsRead)
def update_settings(
    settings_id: int,
    payload: schemas.TestSettingsUpdate,
    service: TestSettingsService = Depends(get_test_settings_service),
):
    settings = service.get_settings(settings_id)
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found"
        )
    return service.update_settings(settings, payload)


@router.delete("/settings/{settings_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_settings(
    settings_id: int,
    service: TestSettingsService = Depends(get_test_settings_service),
):
    settings = service.get_settings(settings_id)
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found"
        )
    service.delete_settings(settings)


# MockTest Endpoints
@router.get("/mock-tests", response_model=list[schemas.MockTestRead])
def list_mock_tests(service: MockTestService = Depends(get_mock_test_service)):
    return service.list_mock_tests()


@router.get("/mock-tests/user/{user_id}", response_model=list[schemas.MockTestRead])
def list_mock_tests_by_user(
    user_id: int,
    service: MockTestService = Depends(get_mock_test_service),
):
    return service.list_mock_tests_by_user(user_id)


@router.get("/mock-tests/{mock_test_id}", response_model=schemas.MockTestRead)
def get_mock_test(
    mock_test_id: int,
    service: MockTestService = Depends(get_mock_test_service),
):
    mock_test = service.get_mock_test(mock_test_id)
    if not mock_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MockTest not found"
        )
    return mock_test


@router.post(
    "/mock-tests",
    response_model=schemas.MockTestRead,
    status_code=status.HTTP_201_CREATED,
)
def create_mock_test(
    payload: schemas.MockTestCreate,
    service: MockTestService = Depends(get_mock_test_service),
):
    return service.create_mock_test(payload)


@router.patch("/mock-tests/{mock_test_id}", response_model=schemas.MockTestRead)
def update_mock_test(
    mock_test_id: int,
    payload: schemas.MockTestUpdate,
    service: MockTestService = Depends(get_mock_test_service),
):
    mock_test = service.get_mock_test(mock_test_id)
    if not mock_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MockTest not found"
        )
    return service.update_mock_test(mock_test, payload)


@router.delete("/mock-tests/{mock_test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mock_test(
    mock_test_id: int,
    service: MockTestService = Depends(get_mock_test_service),
):
    mock_test = service.get_mock_test(mock_test_id)
    if not mock_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MockTest not found"
        )
    service.delete_mock_test(mock_test)
