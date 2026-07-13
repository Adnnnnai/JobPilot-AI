from fastapi import FastAPI

from app.core.database import Base
from app.core.database import engine

# 导入模型，否则不会建表
from app.models.user import User
from app.models.resume import Resume
from app.models.match_record import MatchRecord
from app.models.rewrite_record import RewriteRecord
from app.models.memory import UserProfile
from app.models.memory import UserPreference
from app.models.memory import ExperienceRecord

# 导入路由
from app.api.v1.auth import router as auth_router
from app.api.v1.resume import router as resume_router
from app.api.v1.agent import router as agent_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobPilot AI",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(agent_router)


@app.get("/")
def root():
    return {
        "message": "JobPilot AI Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
