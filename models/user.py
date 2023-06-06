from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from db.session import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(40), unique=True)
    username = Column(String(40), unique=True)
    firstname = Column(String(40))
    lastname = Column(String(40))
    password = Column(String(255))
    is_active = Column(Boolean, default=False)
    role = Column(String(50))
