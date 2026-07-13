from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.user import (
    UserRegister,
    UserLogin,
    Token
)

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    try:

        AuthService.register(
            db,
            user.username,
            user.email,
            user.password
        )

        return {
            "message": "Register Success"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    token = AuthService.login(
        db,
        user.email,
        user.password
    )

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
