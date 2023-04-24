from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import validator
from .. import db
from ..users import service
from ..users.schema import UserRequestModel

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: UserRequestModel, database: Session = Depends(db.get_db)):
    await validator.verify_email_exist(request.email, database)
    return await service.create_user(request=request, database=database)
