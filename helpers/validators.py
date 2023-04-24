from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import api.users.models as users_models
import api.users.schema as users_schema


async def validate_current_user(database: Session,
                                current_user: users_schema.TokenResponse) -> users_models.User:
    user: users_models.User = database.query(users_models.User).get(current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user
