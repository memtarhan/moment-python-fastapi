from datetime import datetime

from sqlalchemy import Column, BigInteger, Text, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db import Base


class Snap(Base):
    __tablename__ = "snaps"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    caption = Column(Text, nullable=True)

    contents = relationship("SnapContent", back_populates="snap")

    creator_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"))
    creator = relationship("User", back_populates="snaps")

    def dict(self) -> {}:
        return self.__dict__


class SnapContent(Base):
    __tablename__ = "snapshot_content"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    photo_url = Column(String, nullable=True)

    snap_id = Column(BigInteger, ForeignKey('snaps.id', ondelete="CASCADE"))
    snap = relationship("Snap", back_populates="contents")

    def dict(self) -> {}:
        return self.__dict__
