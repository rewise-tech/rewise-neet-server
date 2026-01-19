from __future__ import annotations

from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.domain.test.models import TestSettings, MockTest
from app.domain.questions.models import Question
from app.domain.subjects.models import Subject, Chapter


class TestRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_questions_by_subject(self, subject_name: str) -> list[Question]:
        subquery = (
            self.session.query(
                Question.id.label("qid"),
                func.row_number()
                .over(partition_by=Question.chapter, order_by=func.random())
                .label("rn"),
                Chapter.no_of_questions.label("limit"),
            )
            .join(Chapter, Chapter.formatted_name == Question.chapter)
            .join(Subject, Subject.id == Chapter.subject_id)
            .filter(Subject.subject_name == subject_name)
            .subquery()
        )

        return (
            self.session.query(Question)
            .join(subquery, Question.id == subquery.c.qid)
            .filter(subquery.c.rn <= subquery.c.limit)
            .all()
        )


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


class MockTestRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[MockTest]:
        stmt = select(MockTest).order_by(MockTest.id)
        return list(self.session.scalars(stmt))

    def list_by_user(self, user_id: int) -> list[MockTest]:
        stmt = select(MockTest).where(MockTest.user_id == user_id).order_by(MockTest.id)
        return list(self.session.scalars(stmt))

    def get(self, mock_test_id: int) -> Optional[MockTest]:
        return self.session.get(MockTest, mock_test_id)

    def create(self, mock_test: MockTest) -> MockTest:
        self.session.add(mock_test)
        self.session.commit()
        self.session.refresh(mock_test)
        return mock_test

    def update(self, mock_test: MockTest, **fields) -> MockTest:
        for key, value in fields.items():
            if value is not None:
                setattr(mock_test, key, value)

        self.session.add(mock_test)
        self.session.commit()
        self.session.refresh(mock_test)
        return mock_test

    def delete(self, mock_test: MockTest) -> None:
        self.session.delete(mock_test)
        self.session.commit()
