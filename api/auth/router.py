from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import service
from . import validator
from .. import db
from ..users.schema import UserRequestModel

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: UserRequestModel, database: Session = Depends(db.get_db)):
    await validator.verify_email_exist(request.email, database)
    return await service.register(request=request, database=database)


@router.post("/signin")
async def signin(request: OAuth2PasswordRequestForm = Depends(),
                 database: Session = Depends(db.get_db)):
    return await service.signin(request=request, database=database)
