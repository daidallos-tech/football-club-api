from datetime import timedelta, UTC, datetime

from fastapi import BackgroundTasks

from football_club_api.schemas import UserCreate, UserPublic, UserPrivate
from football_club_api.repositories import UserRepository
from football_club_api.models import User, Token, PasswordResetToken
from football_club_api.security import hash_password, verify_password, create_access_token, generate_reset_token, hash_reset_token
from football_club_api.db import settings

from football_club_api.utils import send_password_reset_email

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> UserPrivate:

        if await self.user_repo.get_by_username_lower(user_data.username):
            raise ValueError("Username already exists")

        if await self.user_repo.get_by_email_lower(user_data.email):
            raise ValueError("Email already exists")

        hashed_password = hash_password(user_data.password)

        db_user = await self.user_repo.create_user(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )

        return UserPrivate.model_validate(db_user)

    async def authenticate_user(self, login_input: str, password_input: str) -> Token: 

        user = await self.user_repo.get_user_by_email_or_username(login_input)

        if not user or not verify_password(password_input, user.password_hash):
            raise ValueError("Invalid email or password")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires,
        )
        
        return Token(access_token=access_token, token_type="bearer")

    async def reset_forgotten_user_password(self, email_input: str, background_tasks: BackgroundTasks
    ) -> None: 
        """ Delete and reset token """
        clean_email = email_input.strip().lower()
        user = await self.user_repo.get_user_by_email_or_username(clean_email)

        if user:
            await self.user_repo.delete_existing_token(user.id)

            token = generate_reset_token()
            token_hash = hash_reset_token(token)
            expires_at = datetime.now(UTC) + timedelta(
                minutes=settings.reset_token_expire_minutes,
            )

            reset_token = PasswordResetToken(
                user_id=user.id,
                token_hash=token_hash,
                expires_at=expires_at,
            )
            
            await self.user_repo.save_reset_token(reset_token)

            background_tasks.add_task(
                send_password_reset_email,
                to_email=user.email,
                username=user.username,
                token=token,
            )

