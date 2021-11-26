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

class ModifyPostInfo(BaseModel):
    title: str = None
    content: str = None