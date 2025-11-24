from typing import List

from pydantic import BaseModel, EmailStr, HttpUrl


class UserRegistry(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class Message(BaseException):
    message: str


class URLCreate(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    id: int
    short_code: str
    original_url: str

    class Config:
        from_attributes = True


class URlList(BaseModel):
    urls: List[URLResponse]
