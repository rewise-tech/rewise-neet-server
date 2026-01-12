from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.test.models import TestSettings


class TestSettingsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[TestSettings]:
        stmt = select(TestSettings).order_by(TestSettings.id)
        return list(self.session.scalars(stmt))

    def get(self, settings_id: int) -> Optional[TestSettings]:
        return self.session.get(TestSettings, settings_id)

    def get_by_key(self, key: str) -> Optional[TestSettings]:
        stmt = select(TestSettings).where(TestSettings.key == key)
        return self.session.scalars(stmt).first()

    def create(self, settings: TestSettings) -> TestSettings:
        self.session.add(settings)
        self.session.commit()
        self.session.refresh(settings)
        return settings

    def update(self, settings: TestSettings, **fields) -> TestSettings:
        for key, value in fields.items():
            if value is not None:
                setattr(settings, key, value)

        self.session.add(settings)
        self.session.commit()
        self.session.refresh(settings)
        return settings

    def delete(self, settings: TestSettings) -> None:
        self.session.delete(settings)
        self.session.commit()
