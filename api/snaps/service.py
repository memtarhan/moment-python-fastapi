from typing import List

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import update
from sqlalchemy.orm import Session

import api.users.models as users_models
import api.users.schema as users_schema
import upload.upload_photos as upload_photos
from helpers.validators import validate_current_user
from .models import Snap, SnapContent
from .schema import SnapRequest, SnapResponse


async def get(snap_id: int, database: Session):
    snap: Snap = database.query(Snap).get(snap_id)
    contents: List[SnapContent] = snap.contents
    data = {'caption': snap.caption}
    contents_data = []
    for content in contents:
        contents_data.append({'photo_url': content.photo_url})
    data['contents'] = contents_data
    return SnapResponse.parse_obj(data)


async def create(request: SnapRequest,
                 database: Session,
                 current_user: users_schema.TokenResponse):
    user: users_models.User = await validate_current_user(current_user=current_user, database=database)

    snap_request = jsonable_encoder(request)
    snap_request['creator_id'] = user.id

    snap = Snap(**snap_request)
    database.add(snap)
    database.commit()
    database.refresh(snap)

    return snap


async def create_post_content(snap_id: int,
                              files: List[UploadFile],
                              database: Session):
    # TODO: Validate post here
    for index, fileobject in enumerate(files):
        post_content = SnapContent(snap_id=snap_id)

        database.add(post_content)
        database.commit()
        database.refresh(post_content)

        url = await upload_photos.upload_photo(folder_name="snap_content",
                                               public_id=f"{post_content.id}",
                                               fileobject=fileobject)

        database.execute(
            update(SnapContent).
            where(SnapContent.id == post_content.id).
            values(photo_url=url)
        )

        database.commit()
