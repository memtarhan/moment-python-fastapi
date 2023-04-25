from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from . import schema
from . import service
from .. import db
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/photos", tags=["Photo"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(request: schema.PhotoPostRequestModel,
                      fileobjects: List[UploadFile] = File(...),
                      database: Session = Depends(db.get_db),
                      current_user=Depends(get_current_user)):
    return await service.create_post(request=request,
                                     fileobjects=fileobjects,
                                     database=database,
                                     current_user=current_user)
