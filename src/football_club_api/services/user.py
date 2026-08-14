from football_club_api.schemas import UserPublic, UserPrivate
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