from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from . import service
from .schema import PhotoPostRequestModel
from .. import db
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/photos", tags=["Photo"])


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
async def get(post_id: int,
              database: Session = Depends(db.get_db),
              current_user=Depends(get_current_user)):
    return await service.get_post(post_id=post_id,
                                  database=database,
                                  current_user=current_user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: PhotoPostRequestModel,
                 database: Session = Depends(db.get_db),
                 current_user=Depends(get_current_user)):
    return await service.create_post(request=request,
                                     database=database,
                                     current_user=current_user)


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
async def create_post_content(post_id: int,
                              fileobjects: List[UploadFile] = File(...),
                              database: Session = Depends(db.get_db),
                              current_user=Depends(get_current_user)):
    return await service.create_post_content(post_id=post_id,
                                             fileobjects=fileobjects,
                                             database=database)
