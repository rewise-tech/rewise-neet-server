from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from app.db.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    class_name = Column(String, nullable=False)  # Corresponds to "class" in JSON
    subject_name = Column(String, nullable=False)  # Corresponds to "subject" in JSON

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    chapters = relationship(
        "Chapter", back_populates="subject", cascade="all, delete-orphan"
    )


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True)
    no = Column(String, nullable=False)  # Chapter number (as string, e.g., "1" or "01")
    name = Column(String, nullable=False)  # Chapter name

    subject_id = Column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    subject = relationship("Subject", back_populates="chapters")

    topics = relationship(
        "Topic", back_populates="chapter", cascade="all, delete-orphan"
    )


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    no = Column(String, nullable=False)  # Topic number (as string)
    name = Column(String, nullable=False)  # Topic name

    chapter_id = Column(
        Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False
    )
    chapter = relationship("Chapter", back_populates="topics")
