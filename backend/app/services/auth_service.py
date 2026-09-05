from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse
from app.models.user import User

user_repo = UserRepository()


class AuthService:
    def register(self, db: Session, data: UserCreate) -> User:
        if user_repo.get_by_email(db, data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
        )
        return user_repo.create(db, user)

    def login(self, db: Session, email: str, password: str) -> TokenResponse:
        user = user_repo.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    def refresh(self, db: Session, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        user = user_repo.get(db, payload.get("sub"))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )


auth_service = AuthService()
