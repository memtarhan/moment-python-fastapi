from typing import Optional

from pydantic import BaseModel


class PhotoPostRequestModel(BaseModel):
    caption: Optional[str]

    class Config:
        orm_mode = True


class PhotoPostResponseModel(BaseModel):
    caption: Optional[str]

    class Config:
        orm_mode = True
