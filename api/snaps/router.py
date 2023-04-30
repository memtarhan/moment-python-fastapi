from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from . import service
from .schema import SnapRequest
from .. import db
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/snaps", tags=["Photo"])


@router.get("/{snap_id}", status_code=status.HTTP_200_OK)
async def get(snap_id: int,
              database: Session = Depends(db.get_db),
              current_user=Depends(get_current_user)):
    return await service.get(snap_id=snap_id, database=database)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: SnapRequest,
                 database: Session = Depends(db.get_db),
                 current_user=Depends(get_current_user)):
    return await service.create(request=request,
                                database=database,
                                current_user=current_user)


@router.post("/{snap_id}", status_code=status.HTTP_201_CREATED)
async def upload_photos(snap_id: int,
                        files: List[UploadFile] = File(...),
                        database: Session = Depends(db.get_db)):
    return await service.create_post_content(snap_id=snap_id,
                                             files=files,
                                             database=database)
