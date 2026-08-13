from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from football_club_api.models import User

class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def create_user(self, username: str, email: str, password_hash: str) -> User:
        """ Create new user """

        new_user = User(
            username=username,
            email=email.lower(),
            password_hash=password_hash
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_by_username_lower(self, username: str) -> User | None:
        """ Search user by username """
        result = await self.session.execute(
            select(User).where(func.lower(User.username) == username.lower())
        )
        return result.scalars().first()

    async def get_by_email_lower(self, email: str) -> User | None:
        """ Search user by email """
        result = await self.session.execute(
            select(User).where(func.lower(User.email) == email.lower())
        )
        return result.scalars().first()

    async def get_user_by_user_id(self, user_id: int) -> User | None:
        """ Search user by user id """
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()