from typing import Optional
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Date, String, Text, Boolean

from app.extensions import db

class ApplicationDocument(db.Model):

	__tablename__="application_documents"

	id: Mapped[int] = mapped_column(primary_key=True)

	job_application_id: Mapped[int] = mapped_column(
		ForeignKey("job_applications.id", ondelete="CASCADE"),
		nullable=False,
		index=True
	)

	document_type: Mapped[str] = mapped_column(
		String(80),
		nullable=False
	)

	original_filename: Mapped[str] = mapped_column(
		String(255),
		nullable=False
	)

	stored_filename: Mapped[str] = mapped_column(
		String(255),
		nullable=False
	)

	filepath: Mapped[str] = mapped_column(
		String(500),
		nullable=False
	)

	uploaded_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(timezone.utc),
		nullable=False
	)

	application: Mapped["JobApplication"] = relationship(
		"JobApplication",
		back_populates="documents"
	)
