from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from ..models import Base

from sqlalchemy.sql import func


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=True, nullable=False)
    size = Column(Float(10,2), unique=False, index=True, nullable=False)
    path = Column(String, ForeignKey("folders.path"), unique=False, index=True, nullable=False)
    extension = Column(String, unique=False, index=True, nullable=False)

    datetime = Column(DateTime(timezone=True), server_default=func.now())
    is_del = Column(Boolean, unique=False, default=False)

    tg_id = Column(String, unique=True)

    