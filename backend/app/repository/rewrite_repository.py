from sqlalchemy.orm import Session

from app.models.rewrite_record import RewriteRecord


class RewriteRepository:

    @staticmethod
    def create(
        db: Session,
        rewrite: RewriteRecord
    ):
        db.add(rewrite)
        db.commit()
        db.refresh(rewrite)
        return rewrite

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int
    ):
        return (
            db.query(RewriteRecord)
            .filter(RewriteRecord.user_id == user_id)
            .order_by(RewriteRecord.created_at.desc())
            .all()
        )
