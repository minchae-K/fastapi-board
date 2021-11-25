from fastapi import APIRouter
from pydantic import BaseModel

from sqlalchemy.orm import sessionmaker
from board.repositories import Base, engine
from board.repositories.models import DBUser

router = APIRouter()

Session = sessionmaker(bind=engine)

class MakeSession:
    session = None

    def __enter__(self):
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

class User(BaseModel):
    name: str
    email: str
    password: str

@router.get("/")
def test():
    return "test"

@router.post("/join_user")
def joinUser(user: User):
    Base.metadata.create_all(engine)

    with MakeSession() as session:
        new_user = DBUser()
        new_user.name = user.name
        new_user.email = user.email
        new_user.password = user.password

        session.add(new_user)
        session.commit()

        user1 = session.query(DBUser).first()
    return user1