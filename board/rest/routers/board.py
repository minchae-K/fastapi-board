from fastapi import APIRouter

from sqlalchemy.orm import sessionmaker

from board.repositories import engine
from board.repositories.base import Base
from board.repositories.models import DBUser, DBPost

from datetime import datetime

from board.rest.models.board import User, Post, ModifyUserInfo

router = APIRouter()

# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine) #db 사용을 위한 session 연결

class MakeSession:
    session = None
    #session 사용을 위한 open/close를 python context를 이용하여 설정

    def __enter__(self):
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


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

        result = session.query(DBUser).all()
    return result

@router.put("/modify_user")
def modifyUser(user_id: int, info: ModifyUserInfo):
    #user data 수정
    with MakeSession() as session:
        user = session.query(DBUser).filter_by(id=user_id).first()
        #filter_by로 넣으면 like 연산으로 들어가는 것?

        if info.name != None:
            user.name = info.name
        if info.password != None:
            user.password = info.password

        session.add(user)
        session.commit()
    return user

@router.post("/upload_post")
def uploadPost(post: Post):
    Base.metadata.create_all(engine)

    # #post한 내용 등록
    # with MakeSession() as session:
    #     new_post = DBPost()
    #     new_post.user_id = post.user_id
    #     new_post.title = post.title
    #     new_post.content = post.content
    #     new_post.updated_at = datetime.utcnow()
    #
    #     session.add(new_post)
    #     session.commit()
    #
    #     result = session.query(DBPost).all()
    #
    # return result