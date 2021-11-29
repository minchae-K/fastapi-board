from fastapi import APIRouter

from sqlalchemy.orm import sessionmaker

from board.repositories import engine
from board.repositories.models import DBPost, DBUser

from datetime import datetime

from board.rest.models.board import Post, ModifyPostInfo, ResPost

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


@router.get("/all_post")
def getAllPost():
    with MakeSession() as session:
        posts = session.query(DBPost).all()
        if posts is None:
            return 'post가 존재하지 않습니다.'
        res = []
        for post in posts:
            name = session.query(DBUser.name).filter_by(id=post.user_id).first()
            modify = False if post.created_at.strftime("%m/%d/%Y, %H:%M:%S") == post.updated_at.strftime("%m/%d/%Y, %H:%M:%S") else True
            res.append(ResPost(user_name=name[0], title=post.title, content=post.content, modified=modify))

    return res

@router.get("/id_posts/{user_id}")
def getPostById(user_id: int):
    with MakeSession() as session:
        posts = session.query(DBPost).filter_by(user_id=user_id).all()
        if posts is None:
            return 'post가 존재하지 않습니다.'
        res = []
        for post in posts:
            name = session.query(DBUser.name).filter_by(id=post.user_id).first()
            modify = True if post.created_at.strftime("%m/%d/%Y, %H:%M") == post.updated_at.strftime(
                "%m/%d/%Y, %H:%M") else False
            res.append(ResPost(user_name=name[0], title=post.title, content=post.content, modified=modify))

    return res


@router.post("/upload_post")
def uploadPost(post: Post):
    # Base.metadata.create_all(engine)

    #post한 내용 등록
    with MakeSession() as session:
        new_post = DBPost()
        new_post.user_id = post.user_id
        new_post.title = post.title
        new_post.content = post.content

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

        post.updated_at = datetime.utcnow()
        session.add(post)
        session.commit()
