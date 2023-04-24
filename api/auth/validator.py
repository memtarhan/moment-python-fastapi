from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..users.models import User


async def verify_email_exist(email: str, db_session: Session):
    user = db_session.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="This email is already taken")
