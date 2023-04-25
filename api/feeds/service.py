from sqlalchemy.orm import Session

import api.users.models as users_models
import api.users.schema as users_schema
from helpers.validators import validate_current_user
from .schema import HomeFeedResponse, HomeFeedsResponse
from ..photos.models import PhotoPost


async def get_home_feeds(page: int,
                         limit: int,
                         database: Session,
                         current_user: users_schema.TokenResponse):
    _: users_models.User = await validate_current_user(current_user=current_user, database=database)
    posts: [PhotoPost] = database.query(PhotoPost) \
        .order_by(PhotoPost.created_date.desc()) \
        .limit(limit) \
        .offset((page - 1) * limit) \
        .all()

    data = []

    # Modifying response
    # TODO: implement like & bookmark logic
    for post in posts:
        content_data = []
        for content in post.content:
            content_data.append({
                'liked': True,
                'likes_count': 12,
                'bookmarked': False,
                'bookmarks_count': 4,
                'photo_url': content.photo_url
            })

        post_data = {
            'id': post.id,
            'caption': post.caption,
            'content': content_data
        }
        data.append(HomeFeedResponse.parse_obj(post_data))

    return HomeFeedsResponse.parse_obj({'items': data})
