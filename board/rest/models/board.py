from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str

class ModifyUserInfo(BaseModel):
    name: str = None
    password: str = None

class Post(BaseModel):
    title: str
    content: str