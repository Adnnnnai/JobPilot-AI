from .base_tool import BaseTool

from app.services.resume_service import ResumeService


class ResumeTool(BaseTool):

    name = "resume_analyzer"

    description = "Analyze Resume"

    def run(self, filepath):

        return ResumeService.parse_resume(filepath)
