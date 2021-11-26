from fastapi import APIRouter

from sqlalchemy.orm import sessionmaker

from board.repositories import engine
from board.repositories.models import DBPost

from datetime import datetime

from board.rest.models.board import Post, ModifyPostInfo

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
def l7ConnectionCheck():
    return "success"


@router.post("/upload_post")
def uploadPost(post: Post):
    # Base.metadata.create_all(engine)

    #post한 내용 등록
    with MakeSession() as session:
        new_post = DBPost()
        new_post.user_id = post.user_id
        new_post.title = post.title
        new_post.content = post.content
        new_post.updated_at = datetime.utcnow()

        session.add(new_post)
        session.commit()

        result = session.query(DBPost).all()

    return result

@router.put('/modify_post')
def modifyPost(post_id: int, info: ModifyPostInfo):

    with MakeSession() as session:
        post = session.query(DBPost).filter_by(id=post_id).first()

        if info.title != None:
            post.title = info.title
        if info.content != None:
            post.content = info.content

        session.add(post)
        session.commit()
