from datetime import datetime

from sqlalchemy import Column, BigInteger, Text, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db import Base


class PhotoPost(Base):
    __tablename__ = "photo_posts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    caption = Column(Text, nullable=True)

    content = relationship("PhotoContentPost", back_populates="post")

    creator_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"))
    creator = relationship("User", back_populates="posts")

    def dict(self) -> {}:
        return self.__dict__


class PhotoContentPost(Base):
    __tablename__ = "photo_content_posts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    photo_url = Column(String, nullable=True)

    post_id = Column(BigInteger, ForeignKey('photo_posts.id', ondelete="CASCADE"))
    post = relationship("PhotoPost", back_populates="content")

    def dict(self) -> {}:
        return self.__dict__
