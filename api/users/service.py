from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from helpers.validators import validate_current_user
from ..users.models import User
from ..users.schema import UserResponseModel, TokenResponse


async def get_user(user_id: int, database: Session, current_user: TokenResponse) -> UserResponseModel:
    _: User = await validate_current_user(current_user=current_user, database=database)
    user: User = database.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user
