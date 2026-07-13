from sqlalchemy.orm import Session

from app.models.match_record import MatchRecord


class MatchRepository:

    @staticmethod
    def create(
        db: Session,
        match: MatchRecord
    ):
        db.add(match)
        db.commit()
        db.refresh(match)
        return match

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int
    ):
        return (
            db.query(MatchRecord)
            .filter(MatchRecord.user_id == user_id)
            .order_by(MatchRecord.created_at.desc())
            .all()
        )
