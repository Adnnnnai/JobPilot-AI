from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.resume import AnalyzeRequest

from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume"]
)


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    resume = ResumeService.upload(
        db,
        user_id=1,
        file=file
    )

    return {
        "message": "Upload Success",
        "filename": resume.filename
    }


@router.post("/analyze")
def analyze_resume(
    req: AnalyzeRequest,
    db: Session = Depends(get_db)
):

    try:
        result = ResumeService.analyze(
            db,
            req.resume_id
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
