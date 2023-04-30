import requests
from sqlalchemy.orm import Session

import api.users.models as users_models
import api.users.schema as users_schema
from helpers.validators import validate_current_user
from .schema import HomeFeedResponse, HomeFeedsResponse
from .. import config
from ..snaps.models import Snap


async def get_home_feeds(page: int,
                         limit: int,
                         database: Session,
                         current_user: users_schema.TokenResponse):
    _: users_models.User = await validate_current_user(current_user=current_user, database=database)
    posts: [Snap] = database.query(Snap) \
        .order_by(Snap.created_date.desc()) \
        .limit(limit) \
        .offset((page - 1) * limit) \
        .all()

    data = []

    # Modifying response
    # TODO: implement like & bookmark logic
    for post in posts:
        content_data = []
        for content in post.contents:
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


async def get_popular_movies(page: int):
    url = f"{config.MOVIES_API_BASE_URL}/movie/popular?api_key={config.MOVIES_API_KEY}&language=en-US&page={page}"

    response = requests.get(url)

    response_json = response.json()
    results = response_json['results']
    return results
