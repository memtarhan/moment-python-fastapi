from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import api.auth.hashing as hashing
from ..users.models import User
from ..users.schema import UserRequestModel, UserResponseModel


async def create_user(request: UserRequestModel, database: Session) -> UserResponseModel:
    user_request = jsonable_encoder(request)
    password = user_request["password"]
    user_request["password"] = hashing.get_password_hash(password)

    user = User(**user_request)
    database.add(user)
    database.commit()
    database.refresh(user)

    return UserResponseModel.from_orm(user)
