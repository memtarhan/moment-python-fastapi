from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class HomeFeedContentResponse(BaseModel):
    liked: bool
    likes_count: int
    bookmarked: bool
    bookmarks_count: int
    photo_url: Optional[HttpUrl]


class HomeFeedResponse(BaseModel):
    id: int
    caption: Optional[str]
    content: List[HomeFeedContentResponse]


class HomeFeedsResponse(BaseModel):
    items: List[HomeFeedResponse]
