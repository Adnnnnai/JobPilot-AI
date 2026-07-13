import json


class ResumeChunker:

    @staticmethod
    def split(resume_text: str) -> list[str]:
        return [c for c in resume_text.split("\n\n") if c.strip()]

    @staticmethod
    def from_json(resume_json: dict) -> list[str]:
        text = json.dumps(resume_json, ensure_ascii=False, indent=2)
        return ResumeChunker.split(text)
