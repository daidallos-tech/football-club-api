from football_club_api.schemas import UserPublic, UserPrivate, UserUpdate
from football_club_api.repositories import UserRepository
from football_club_api.security import CurrentUser

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user_profile_by_id(self, user_id: int) -> UserPublic:
        user = await self.user_repo.get_user_by_user_id(user_id)
        
        if not user:
            raise ValueError("User not found")
            
        return UserPublic.model_validate(user)

    async def get_current_user(self, current_user: CurrentUser) -> UserPrivate:
        return UserPrivate.model_validate(current_user)

    async def partial_update_user_profile(self, current_user: CurrentUser, user_update: UserUpdate) -> UserPrivate:
        db_user = await self.user_repo.get_user_by_user_id(current_user.id)
        if not db_user:
            raise ValueError("User not found")

        update_data = user_update.model_dump(exclude_unset=True)

        if "username" in update_data:
            new_username = update_data["username"].strip().lower()
            if new_username != db_user.username:
                if await self.user_repo.get_user_by_email_or_username(new_username):
                    raise ValueError("Username already exists")
            update_data["username"] = new_username

        if "email" in update_data:
            new_email = update_data["email"].strip().lower()
            if new_email != db_user.email:
                if await self.user_repo.get_user_by_email_or_username(new_email):
                    raise ValueError("Email already exists")
            update_data["email"] = new_email

        updated_db_user = await self.user_repo.update_user(db_user, update_data)
        
        return UserPrivate.model_validate(updated_db_user)

    async def delete_user(self, current_user: CurrentUser) -> None:
        db_user = await self.user_repo.get_user_by_user_id(current_user.id)

        if not db_user:
            raise ValueError("User not found")

        await self.user_repo.delete_user(db_user)
    