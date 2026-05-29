from __future__ import annotations

from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class MockInterviewResponse(db.Model):
    __tablename__ = "mock_interview_responses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("mock_interview_questions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    answer: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    feedback: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    improved_answer: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    question: Mapped["MockInterviewQuestion"] = relationship(
        "MockInterviewQuestion",
        back_populates="mock_interview_responses",
    )