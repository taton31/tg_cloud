from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from ..models import Base

from sqlalchemy.sql import func



class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    path = Column(String, ForeignKey("files.path"), unique=False, index=True, nullable=False)
    path_to = Column(String, ForeignKey("files.path"), unique=False, index=True, nullable=False)

    datetime = Column(DateTime(timezone=True), server_default=func.now())
    is_del = Column(Boolean, unique=False, default=False)


