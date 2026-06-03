from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    MANAGER = "manager"
    


class Permission(str, Enum):
    READ = "posts:read"
    WRITE = "posts:write"
    DELETE = "posts:delete"


class Token(BaseModel):
    access_token: str
    token_type: str
    roles: list[str]


class UserOut(BaseModel):
    username: str
    email: str
    roles: list[str]


class PostCreate(BaseModel):
    title: str
    body: str


class PostOut(BaseModel):
    id: int
    title: str
    body: str
    author: str
