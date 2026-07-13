import json
import os
import shutil

from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.models.resume import Resume

from app.repository.resume_repository import ResumeRepository

from app.services.resume_parser import ResumeParser

from app.services.llm_service import LLMService

from app.utils.text_cleaner import TextCleaner


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)

UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")


class ResumeService:

    @staticmethod
    def upload(
        db: Session,
        user_id: int,
        file: UploadFile
    ):

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )

        filepath = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(
            filepath,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        resume = Resume(
            user_id=user_id,
            filename=file.filename,
            filepath=filepath
        )

        return ResumeRepository.create(
            db,
            resume
        )

    @staticmethod
    def parse_resume(filepath: str):
        text = ResumeParser.parse(filepath)
        text = TextCleaner.clean(text)

        prompt_path = os.path.join(
            PROJECT_ROOT,
            "agent",
            "prompts",
            "resume_parser.md"
        )

        with open(prompt_path, encoding="utf8") as f:
            prompt = f.read()

        prompt += "\n\n"
        prompt += text

        result = LLMService.chat(prompt)

        return json.loads(result)

    @staticmethod
    def analyze(db: Session, resume_id: int):

        resume = ResumeRepository.get_by_id(
            db,
            resume_id
        )

        if not resume:
            raise ValueError("Resume not found")

        try:
            resume.status = "parsing"
            ResumeRepository.update(db, resume)

            text = ResumeParser.parse(resume.filepath)

            text = TextCleaner.clean(text)

            prompt_path = os.path.join(
                PROJECT_ROOT,
                "agent",
                "prompts",
                "resume_parser.md"
            )

            with open(
                prompt_path,
                encoding="utf8"
            ) as f:
                prompt = f.read()

            prompt += "\n\n"
            prompt += text

            result = LLMService.chat(prompt)

            resume.status = "parsed"
            ResumeRepository.update(db, resume)

            return json.loads(result)

        except Exception:
            resume.status = "failed"
            ResumeRepository.update(db, resume)
            raise
