from sqlalchemy import select
from sqlalchemy import delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession
from football_club_api.models import User, PasswordResetToken

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
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def get_by_email_lower(self, email: str) -> User | None:
        """ Search user by email """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_user_by_user_id(self, user_id: int) -> User | None:
        """ Search user by user id """
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()

    async def get_user_by_email_or_username(self, login: str) -> User | None:
        """ Search user by email or username """
        result = await self.session.execute(
            select(User).where(
                (User.email == login) | (User.username == login)
                )
        )
        return result.scalars().first()

    async def update_user(self, db_user: User, update_data: dict) -> User:
        for key, value in update_data.items():
            setattr(db_user, key, value) 

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def delete_user(self, db_user: User) -> None:
        """ Delete user """
        await self.session.delete(db_user)
        await self.session.commit()

    async def delete_existing_token(self, user_id: int) -> None:
        await self.session.execute(
            sql_delete(PasswordResetToken).where(
                PasswordResetToken.user_id == user_id,
            )
        )

    async def save_reset_token(self, reset_token: PasswordResetToken) -> None:
        self.session.add(reset_token)
        await self.session.commit()

    async def get_reset_token_by_hash(self, token_hash: str) -> PasswordResetToken | None:
        result = await self.session.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == token_hash
            )
        )
        return result.scalars().first()

    async def delete_token(self, reset_token: PasswordResetToken) -> None:
        await self.session.delete(reset_token)
        await self.session.commit()

    async def update_user_password(self, user: User, new_password: str) -> None:
        user.password_hash = new_password
        self.session.add(user)

        await self.session.execute(
            sql_delete(PasswordResetToken).where(PasswordResetToken.user_id == user.id)
        )
        await self.session.commit()