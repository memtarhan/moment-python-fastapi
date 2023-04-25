from typing import List

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import update
from sqlalchemy.orm import Session

import api.users.models as users_models
import api.users.schema as users_schema
import upload.upload_photos as upload_photos
from helpers.validators import validate_current_user
from .models import PhotoPost, PhotoContentPost
from .schema import PhotoPostRequestModel


async def get_post(post_id: int,
                   database: Session,
                   current_user: users_schema.TokenResponse):
    post: PhotoPost = database.query(PhotoPost).get(post_id)
    return post


async def create_post(request: PhotoPostRequestModel,
                      database: Session,
                      current_user: users_schema.TokenResponse):
    user: users_models.User = await validate_current_user(current_user=current_user, database=database)

    post_request = jsonable_encoder(request)
    post_request['creator_id'] = user.id

    post = PhotoPost(**post_request)
    database.add(post)
    database.commit()
    database.refresh(post)

    return post


async def create_post_content(post_id: int,
                              fileobjects: List[UploadFile],
                              database: Session):
    # TODO: Validate post here
    for index, fileobject in enumerate(fileobjects):
        post_content = PhotoContentPost(post_id=post_id)

        database.add(post_content)
        database.commit()
        database.refresh(post_content)

        url = await upload_photos.upload_photo(folder_name="post_content",
                                               public_id=f"{post_content.id}",
                                               fileobject=fileobject)

        database.execute(
            update(PhotoContentPost).
            where(PhotoContentPost.id == post_content.id).
            values(photo_url=url)
        )

        database.commit()
