from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import schema
from . import service
from .. import db
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/{user_id}",
            status_code=status.HTTP_200_OK,
            response_model=schema.UserResponseModel)
async def get_user(user_id: int,
                   database: Session = Depends(db.get_db),
                   current_user=Depends(get_current_user)):
    return await service.get_user(user_id=user_id, database=database, current_user=current_user)
