from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import hashing
from .jwt import create_access_token
from ..users.models import User
from ..users.schema import UserRequestModel, UserResponseModel, SigninResponseModel


async def register(request: UserRequestModel, database: Session) -> UserResponseModel:
    user_request = jsonable_encoder(request)
    password = user_request["password"]
    user_request["password"] = hashing.get_password_hash(password)

    user = User(**user_request)
    database.add(user)
    database.commit()
    database.refresh(user)

    return UserResponseModel.from_orm(user)


async def signin(request: OAuth2PasswordRequestForm,
                 database: Session) -> SigninResponseModel:
    user: User = database.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="Invalid credentials")

    # Generate a JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    data = {'access_token': access_token,
            'token_type': 'bearer',
            'profile': UserResponseModel(**user.dict())}
    return SigninResponseModel(**data)
