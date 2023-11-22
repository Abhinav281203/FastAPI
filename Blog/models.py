from database import base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class blog(base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("user", back_populates="blogs")


class user(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("blog", back_populates="creator")
