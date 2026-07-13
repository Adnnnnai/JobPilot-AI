import fitz
from docx import Document


class ResumeParser:

    @staticmethod
    def parse(filepath: str) -> str:

        if filepath.endswith(".pdf"):
            return ResumeParser.parse_pdf(filepath)

        elif filepath.endswith(".docx"):
            return ResumeParser.parse_docx(filepath)

        else:
            raise ValueError("Unsupported file format")

    @staticmethod
    def parse_pdf(filepath: str):

        doc = fitz.open(filepath)

        text = ""

        for page in doc:
            text += page.get_text()

        return text

    @staticmethod
    def parse_docx(filepath: str):

        doc = Document(filepath)

        text = ""

        for p in doc.paragraphs:
            text += p.text + "\n"

        return text
