import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from db.session import Base


class FileInfos(Base):
    __tablename__ = 'fileinfos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    size = Column(String(200))
    src = Column(String(200))
    created_at = Column(sqlalchemy.DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))

