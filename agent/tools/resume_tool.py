import json

from .base_tool import BaseTool

from app.services.resume_service import ResumeService
from app.services.llm_service import LLMService


class ResumeTool(BaseTool):

    name = "resume_analyzer"
    description = "Analyze Resume"

    def run(self, filepath):
        try:
            return ResumeService.parse_resume(filepath)
        except Exception as e:
            return {"name": "", "skills": [], "education": [], "projects": [], "error": str(e)}
