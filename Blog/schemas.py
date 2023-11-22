from pydantic import BaseModel
from typing import List, Optional


class blog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class user(BaseModel):
    username: str
    email: str
    password: str


class showuser(BaseModel):
    username: str
    email: str
    blogs: List[blog]

    class Config:
        orm_mode = True


class blogwithoutid(BaseModel):
    title: str
    body: str
    creator: showuser

    class Config:
        orm_mode = True


class login(BaseModel):
    email: str
    password: str


class token(BaseModel):
    access_token: str
    token_type: str


class tokendata(BaseModel):
    email: str
