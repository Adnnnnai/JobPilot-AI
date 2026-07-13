"""
Memory 服务——四层记忆统一入口

Conversation   → MemorySaver (已有，无需额外代码)
User Profile   → user_profiles 表
Preference     → user_preferences 表
Experience     → experience_records 表
"""
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.memory import UserProfile, UserPreference, ExperienceRecord


def _safe_commit(db: Session, obj, add: bool = False):
    """兼容不同 Session 的提交方式"""
    try:
        if add:
            db.add(obj)
        db.commit()
    except Exception:
        db.rollback()
        # 用 raw SQL 作为 fallback
        if isinstance(obj, UserPreference):
            db.execute(text(
                "INSERT INTO user_preferences (user_id, key, value) "
                "VALUES (:uid, :key, :val) "
                "ON CONFLICT DO NOTHING"
            ), {"uid": obj.user_id, "key": obj.key, "val": obj.value})
            db.commit()
        elif isinstance(obj, ExperienceRecord):
            db.execute(text(
                "INSERT INTO experience_records "
                "(user_id, event_type, version, accepted, meta_json) "
                "VALUES (:uid, :et, :v, :acc, :meta)"
            ), {
                "uid": obj.user_id, "et": obj.event_type,
                "v": obj.version, "acc": obj.accepted,
                "meta": obj.meta_json
            })
            db.commit()
    if add:
        db.refresh(obj)


class MemoryService:

    # ── Profile ──────────────────────────────

    @staticmethod
    def get_profile(db: Session, user_id: int) -> dict:
        profile = (
            db.query(UserProfile)
            .filter(UserProfile.user_id == user_id)
            .first()
        )
        if not profile:
            return {}
        return {
            "target_job": profile.target_job,
            "city": profile.city,
            "salary": profile.salary,
            "education": profile.education,
            "experience_years": profile.experience_years,
        }

    @staticmethod
    def save_profile(db: Session, user_id: int, **kwargs):
        profile = (
            db.query(UserProfile)
            .filter(UserProfile.user_id == user_id)
            .first()
        )
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.add(profile)

        for k, v in kwargs.items():
            if hasattr(profile, k):
                setattr(profile, k, v)

        _safe_commit(db, profile, add=True)
        return profile

    # ── Preferences ───────────────────────────

    @staticmethod
    def get_preferences(db: Session, user_id: int) -> dict:
        prefs = (
            db.query(UserPreference)
            .filter(UserPreference.user_id == user_id)
            .all()
        )
        return {p.key: p.value for p in prefs}

    @staticmethod
    def set_preference(db: Session, user_id: int, key: str, value: str):
        pref = (
            db.query(UserPreference)
            .filter(
                UserPreference.user_id == user_id,
                UserPreference.key == key,
            )
            .first()
        )
        if not pref:
            pref = UserPreference(user_id=user_id, key=key)
            db.add(pref)
        pref.value = value
        _safe_commit(db, pref)
        return pref

    # ── Experience ────────────────────────────

    @staticmethod
    def record_experience(
        db: Session, user_id: int, event_type: str,
        version: int = 1, accepted: bool = False, meta: dict = None
    ):
        record = ExperienceRecord(
            user_id=user_id,
            event_type=event_type,
            version=version,
            accepted=accepted,
            meta_json=str(meta or {}),
        )
        db.add(record)
        _safe_commit(db, record)
        return record

    @staticmethod
    def get_accepted_versions(db: Session, user_id: int, event_type: str) -> list[int]:
        records = (
            db.query(ExperienceRecord)
            .filter(
                ExperienceRecord.user_id == user_id,
                ExperienceRecord.event_type == event_type,
                ExperienceRecord.accepted == True,
            )
            .all()
        )
        return [r.version for r in records]
