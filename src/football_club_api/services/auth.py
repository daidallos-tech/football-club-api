from datetime import timedelta

from football_club_api.schemas import UserCreate, UserPublic, UserPrivate
from football_club_api.repositories import UserRepository
from football_club_api.models import User, Token
from football_club_api.security import hash_password, verify_password, create_access_token
from football_club_api.db import settings

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
        

