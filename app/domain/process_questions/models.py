from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base


class StageQuestion(Base):
    __tablename__ = "stage_questions"

    id = Column(Integer, primary_key=True, index=True)

    # Main fields from the root JSON
    source = Column(String, nullable=False, index=True)
    year = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False, index=True)
    chapter = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False, index=True)
    question_number = Column(String, nullable=False, index=True)

    question_text = Column(Text, nullable=False)
    has_diagram = Column(Boolean, default=False)
    diagram_description = Column(Text)
    diagram_position = Column(String)  # e.g., "above", "below", "inline"
    diagram_name = Column(Text)  # filename or identifier

    answer = Column(String, nullable=False)  # e.g., "B" or "2"
    solution = Column(Text)

    reviewed = Column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    # Relationship to options
    options = relationship(
        "StageOption", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<StageQuestion {self.source} {self.year} #{self.question_number}>"


class StageOption(Base):
    __tablename__ = "stage_options"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to parent stage question
    question_id = Column(Integer, ForeignKey("stage_questions.id"), nullable=False)

    label = Column(String, nullable=False)  # e.g., "A", "B", "1", "2"
    text = Column(Text, nullable=False)

    has_diagram = Column(Boolean, default=False)
    diagram_description = Column(Text)
    diagram_name = Column(Text)

    # Relationship back to stage question
    question = relationship("StageQuestion", back_populates="options")

    def __repr__(self):
        return f"<StageOption {self.label}: {self.text[:50]}...>"
