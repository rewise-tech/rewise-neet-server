from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.test import schemas
from app.domain.test.services import TestSettingsService

router = APIRouter(prefix="/test", tags=["settings"])


def get_test_settings_service(db: Session = Depends(get_db)) -> TestSettingsService:
    return TestSettingsService(db)


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
