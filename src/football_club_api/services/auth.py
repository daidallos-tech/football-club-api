from football_club_api.schemas import UserCreate, UserPublic
from football_club_api.repositories import UserRepository
from football_club_api.models import User
from football_club_api.security import hash_password

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> User:

        if await self.user_repo.get_by_username_lower(user_data.username):
            raise ValueError("Username already exists")

        if await self.user_repo.get_by_email_lower(user_data.email):
            raise ValueError("Email already exists")

        hashed_password = hash_password(user_data.password)

        return await self.user_repo.create_user(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user_profile_by_id(self, user_id: int) -> User:
        user = await self.user_repo.get_user_by_user_id(user_id)
        
        if not user:
            raise ValueError("User not found")
            
        return user