from typing import Optional

from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    id: int
    email: Optional[EmailStr] = None


class UserRequestModel(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    email: str
    password: str
    bio: Optional[str]

    class Config:
        orm_mode = True


class UserResponseModel(BaseModel):
    id: int
    username: Optional[str]
    full_name: Optional[str]
    email: Optional[str]
    bio: Optional[str]
    profile_photo: Optional[str]

    class Config:
        orm_mode = True


class SigninResponseModel(BaseModel):
    access_token: str
    token_type: str
    profile: UserResponseModel
