from typing import List

from fastapi import UploadFile
from sqlalchemy import update
from sqlalchemy.orm import Session

import api.users.models as users_models
import api.users.schema as users_schema
import upload.upload_photos as upload_photos
from helpers.validators import validate_current_user
from .models import PhotoPost, PhotoContentPost
from .schema import PhotoPostRequestModel


async def create_post(request: PhotoPostRequestModel,
                      fileobjects: List[UploadFile],
                      database: Session,
                      current_user: users_schema.TokenResponse):
    user: users_models.User = await validate_current_user(current_user=current_user, database=database)

    post = PhotoPost(caption=request.caption, creator_id=user.id)
    database.add(post)
    database.commit()
    database.refresh(post)

    for index, fileobject in enumerate(fileobjects):
        post_content = PhotoContentPost(post_id=post.id)

        database.add(post_content)
        database.commit()
        database.refresh(post_content)

        url = await upload_photos.upload_photo(folder_name="pets",
                                               public_id=f"{post_content.id}",
                                               fileobject=fileobject)

        database.execute(
            update(PhotoContentPost).
            where(PhotoContentPost.id == post_content.id).
            values(photo_ur=url)
        )

        database.commit()

    database.refresh(post)

    return post
