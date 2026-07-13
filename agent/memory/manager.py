"""
Memory Manager

统一读写四层记忆。所有 Agent 通过这个接口访问记忆，不直接操作 SQL。
"""
import sys
import os

# 确保 backend 模块可导入
BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "backend")
)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.core.database import SessionLocal
from app.services.memory_service import MemoryService as MS


class MemoryManager:
    """统一记忆管理器"""

    @staticmethod
    def _get_db():
        return SessionLocal()

    # ── Profile ──────────────────────────────

    @staticmethod
    def get_profile(user_id: int) -> dict:
        db = MemoryManager._get_db()
        try:
            return MS.get_profile(db, user_id)
        finally:
            db.close()

    @staticmethod
    def save_profile(user_id: int, **kwargs):
        db = MemoryManager._get_db()
        try:
            return MS.save_profile(db, user_id, **kwargs)
        finally:
            db.close()

    # ── Preferences ───────────────────────────

    @staticmethod
    def get_preferences(user_id: int) -> dict:
        db = MemoryManager._get_db()
        try:
            return MS.get_preferences(db, user_id)
        finally:
            db.close()

    @staticmethod
    def set_preference(user_id: int, key: str, value: str):
        db = MemoryManager._get_db()
        try:
            return MS.set_preference(db, user_id, key, value)
        finally:
            db.close()

    # ── Experience ────────────────────────────

    @staticmethod
    def record_experience(user_id: int, event_type: str, version: int = 1, accepted: bool = False, meta: dict = None):
        db = MemoryManager._get_db()
        try:
            return MS.record_experience(db, user_id, event_type, version, accepted, meta)
        finally:
            db.close()

    @staticmethod
    def get_accepted_versions(user_id: int, event_type: str) -> list[int]:
        db = MemoryManager._get_db()
        try:
            return MS.get_accepted_versions(db, user_id, event_type)
        finally:
            db.close()

    @staticmethod
    def get_history(user_id: int, event_type: str = None) -> list[dict]:
        """查询用户历史记录"""
        from app.models.memory import ExperienceRecord
        db = MemoryManager._get_db()
        try:
            q = db.query(ExperienceRecord).filter(ExperienceRecord.user_id == user_id)
            if event_type:
                q = q.filter(ExperienceRecord.event_type == event_type)
            records = q.order_by(ExperienceRecord.created_at.desc()).limit(50).all()
            return [{
                "event_type": r.event_type,
                "version": r.version,
                "accepted": r.accepted,
                "meta": r.meta_json,
                "created_at": str(r.created_at),
            } for r in records]
        finally:
            db.close()

    # ── Load / Save State ─────────────────────

    @staticmethod
    def load(user_id: int) -> dict:
        """加载用户的所有长期记忆到 state"""
        return {
            "profile": MemoryManager.get_profile(user_id),
            "preferences": MemoryManager.get_preferences(user_id),
            "experiences": MemoryManager.get_history(user_id),
        }

    @staticmethod
    def save(state: dict, user_id: int = 1):
        """从 state 中提取值得保留的信息，保存到长期记忆"""
        from .strategy import MemoryStrategy

        message = state.get("message", "")
        if not message or not MemoryStrategy.should_save(message):
            return

        # 提取偏好
        new_prefs = MemoryStrategy.extract_preferences(message)
        for key, value in new_prefs.items():
            MemoryManager.set_preference(user_id, key, value)

        # 保存画像
        profile_fields = state.get("profile", {})
        if profile_fields:
            MemoryManager.save_profile(user_id, **profile_fields)

        # 记录改写经验（含偏好学习）
        if state.get("rewrite_result"):
            MemoryManager.record_experience(
                user_id, "rewrite",
                version=state.get("completed_tasks", []).__len__() + 1,
                accepted=False,
                meta={"message": message}
            )

        # 记录面试经验
        if state.get("interview_questions"):
            MemoryManager.record_experience(
                user_id, "interview",
                meta={"question_count": len(state["interview_questions"])}
            )

    # ── Experience Learning ────────────────────

    @staticmethod
    def learn_preference(user_id: int, event_type: str, version: int):
        from app.models.memory import ExperienceRecord
        from sqlalchemy import text

        db = MemoryManager._get_db()
        try:
            db.execute(text(
                "UPDATE experience_records SET accepted = TRUE "
                "WHERE user_id = :uid AND event_type = :et AND version = :v"
            ), {"uid": user_id, "et": event_type, "v": version})
            db.commit()

            count = db.execute(text(
                "SELECT count(*) FROM experience_records "
                "WHERE user_id = :uid AND event_type = :et AND accepted = TRUE"
            ), {"uid": user_id, "et": event_type}).scalar()

            if count >= 2:
                MemoryManager.set_preference(
                    user_id,
                    f"preferred_{event_type}_version",
                    str(version)
                )
        finally:
            db.close()

    @staticmethod
    def get_learned_style(user_id: int, event_type: str) -> dict:
        """获取用户在某个事件类型上的学习偏好"""
        accepted = MemoryManager.get_accepted_versions(user_id, event_type)
        prefs = MemoryManager.get_preferences(user_id)
        return {
            "accepted_versions": accepted,
            "preferred_version": prefs.get(f"preferred_{event_type}_version"),
        }
