from sqlalchemy.orm import Session

from app.domain.test import schemas
from app.domain.test.models import TestSettings
from app.domain.test.repository import TestSettingsRepository


class TestSettingsService:
    def __init__(self, session: Session) -> None:
        self.repo = TestSettingsRepository(session)

    def list_settings(self) -> list[TestSettings]:
        return self.repo.list()

    def get_settings(self, settings_id: int) -> TestSettings | None:
        return self.repo.get(settings_id)

    def get_settings_by_key(self, key: str) -> TestSettings | None:
        return self.repo.get_by_key(key)

    def create_settings(self, payload: schemas.TestSettingsCreate) -> TestSettings:
        settings = TestSettings(
            key=payload.key,
            value=payload.value,
            is_active=payload.is_active,
        )
        return self.repo.create(settings)

    def update_settings(
        self, settings: TestSettings, payload: schemas.TestSettingsUpdate
    ) -> TestSettings:
        fields: dict[str, object] = {}
        if payload.key is not None:
            fields["key"] = payload.key
        if payload.value is not None:
            fields["value"] = payload.value
        if payload.is_active is not None:
            fields["is_active"] = payload.is_active

        return self.repo.update(settings, **fields)

    def delete_settings(self, settings: TestSettings) -> None:
        self.repo.delete(settings)
