from typing import Final
from pydantic import BaseModel, EmailStr, Field

MIN_LENGTH: Final[int] = 8
MAX_LENGTH: Final[int] = 120

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(max_length=120)

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)