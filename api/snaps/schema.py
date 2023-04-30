from typing import Optional, List

from pydantic import BaseModel


class SnapRequest(BaseModel):
    caption: Optional[str]


class SnapContentResponse(BaseModel):
    photo_url: Optional[str]


class SnapResponse(BaseModel):
    caption: Optional[str]
    contents: List[SnapContentResponse]

    class Config:
        orm_mode = True
