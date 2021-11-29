from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str

class ModifyUserInfo(BaseModel):
    name: str = None
    password: str = None

class Post(BaseModel):
    user_id: int
    title: str
    content: str

class ResPost(BaseModel):
    user_name: str
    title: str
    content: str
    modified: bool

class ModifyPostInfo(BaseModel):
    title: str = None
    content: str = None