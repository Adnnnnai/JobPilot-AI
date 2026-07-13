from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class JobDescription(Base):

    __tablename__ = "job_descriptions"

    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(300), default="", nullable=False
    )

    company: Mapped[str] = mapped_column(
        String(200), default="", nullable=False
    )

    salary: Mapped[str] = mapped_column(
        String(100), default="", nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100), default="", nullable=False
    )

    tech_stack: Mapped[str] = mapped_column(
        Text, default="", nullable=False
    )

    requirements: Mapped[str] = mapped_column(
        Text, default="", nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text, default="", nullable=False
    )

    keywords: Mapped[str] = mapped_column(
        String(300), default="", nullable=False
    )

    source: Mapped[str] = mapped_column(
        String(50), default="llm_generated", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
