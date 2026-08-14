from typing import Final
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

USERNAME_MIN_LENGTH: Final[int] = 5
USERNAME_MAX_LENGTH: Final[int] = 50
EMAIL_MAX_LENGTH: Final[int] = 120
PASSWORD_MIN_LENGTH: Final[int] = 8

class UserBase(BaseModel):
    username: str = Field(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH)
    email: EmailStr = Field(max_length=EMAIL_MAX_LENGTH)

    @field_validator("username", "email", mode="before")
    @classmethod
    def to_lowercase(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

class UserCreate(UserBase):
    password: str = Field(min_length=PASSWORD_MIN_LENGTH)

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    image_file: str | None = None
    image_path: str | None = None

class UserPrivate(UserPublic):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH)
    email: EmailStr | None = Field(default=None, max_length=EMAIL_MAX_LENGTH)