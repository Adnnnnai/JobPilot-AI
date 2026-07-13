from sqlalchemy.orm import Session

from app.models.user import User

from app.repository.user_repository import UserRepository

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        username,
        email,
        password
    ):

        if UserRepository.get_by_email(db, email):
            raise Exception("Email already exists")

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password)
        )

        return UserRepository.create(
            db,
            user
        )

    @staticmethod
    def login(
        db: Session,
        email,
        password
    ):

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash
        ):
            return None

        token = create_access_token(
            {
                "sub": user.email
            }
        )

        return token
