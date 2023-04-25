from fastapi import APIRouter, Depends, status
from fastapi_pagination import add_pagination
from sqlalchemy.orm import Session

from . import service
from .schema import HomeFeedsResponse
from .. import db
from ..auth.jwt import get_current_user

router = APIRouter(tags=["Feed"], prefix="/feeds")


@router.get("/home",
            status_code=status.HTTP_200_OK,
            response_model=HomeFeedsResponse)
async def get_home_feeds(page: int = 1,
                         limit: int = 3,
                         database: Session = Depends(db.get_db),
                         current_user=Depends(get_current_user)):
    """
    Fetches a list of Home Feeds at a given page and with a given limit. Feeds are ordered by create date.
    """
    return await service.get_home_feeds(page=page, limit=limit, database=database, current_user=current_user)


add_pagination(router)
