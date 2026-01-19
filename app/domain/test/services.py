from sqlalchemy.orm import Session

from app.domain.test import schemas
from app.domain.test.models import TestSettings, MockTest
from app.domain.test.repository import (
    TestRepository,
    TestSettingsRepository,
    MockTestRepository,
)

from app.domain.questions.models import Question


class TestService:
    def __init__(self, session: Session) -> None:
        self.repo = TestRepository(session)

    def prepare_test(self) -> list[Question]:
        questions_list = []
        physics_questions = self.repo.get_questions_by_subject("Physics")
        chemistry_questions = self.repo.get_questions_by_subject("Chemistry")
        biology_questions = self.repo.get_questions_by_subject("Biology")

        questions_list.extend(physics_questions)
        questions_list.extend(chemistry_questions)
        questions_list.extend(biology_questions)

        return questions_list

    def get_questions_by_subject(self, subject_name: str) -> list[Question]:
        return self.repo.get_questions_by_subject(subject_name)


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


class MockTestService:
    def __init__(self, session: Session) -> None:
        self.repo = MockTestRepository(session)

    def list_mock_tests(self) -> list[MockTest]:
        return self.repo.list()

    def list_mock_tests_by_user(self, user_id: int) -> list[MockTest]:
        return self.repo.list_by_user(user_id)

    def get_mock_test(self, mock_test_id: int) -> MockTest | None:
        return self.repo.get(mock_test_id)

    def create_mock_test(self, payload: schemas.MockTestCreate) -> MockTest:
        mock_test = MockTest(
            marks_scored=payload.marks_scored,
            test_status=payload.test_status,
            questions=payload.questions,
            time_taken=payload.time_taken,
            user_id=payload.user_id,
        )
        return self.repo.create(mock_test)

    def update_mock_test(
        self, mock_test: MockTest, payload: schemas.MockTestUpdate
    ) -> MockTest:
        fields: dict[str, object] = {}
        if payload.marks_scored is not None:
            fields["marks_scored"] = payload.marks_scored
        if payload.test_status is not None:
            fields["test_status"] = payload.test_status
        if payload.questions is not None:
            fields["questions"] = payload.questions
        if payload.time_taken is not None:
            fields["time_taken"] = payload.time_taken

        return self.repo.update(mock_test, **fields)

    def delete_mock_test(self, mock_test: MockTest) -> None:
        self.repo.delete(mock_test)
