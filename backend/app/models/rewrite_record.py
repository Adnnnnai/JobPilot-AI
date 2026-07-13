from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class RewriteRecord(Base):

    __tablename__ = "rewrite_records"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))

    original_json: Mapped[str] = mapped_column(Text)

    rewrite_result: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
