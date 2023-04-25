from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.orm import relationship

from ..db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(63), unique=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    profile_photo = Column(String, nullable=True)

    posts = relationship("PhotoPost", back_populates="creator")

    def dict(self) -> {}:
        return self.__dict__
