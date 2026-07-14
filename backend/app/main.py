"""
JobPilot AI - Simplified Backend Entry Point

Removes LangGraph workflow complexity in favor of direct API handling.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine

# Import models for table creation
from app.models.user import User
from app.models.resume import Resume
from app.models.match_record import MatchRecord
from app.models.rewrite_record import RewriteRecord
from app.models.memory import UserProfile, UserPreference, ExperienceRecord
from app.models.job_description import JobDescription

# Import routers
from app.api.v1.auth import router as auth_router
from app.api.v1.resume import router as resume_router
from app.api.v1.agent import router as agent_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobPilot AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(agent_router)


@app.get("/")
def root():
    return {"message": "JobPilot AI Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}
