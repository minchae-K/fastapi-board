from fastapi import APIRouter

from board.repositories import MakeSession
from board.repositories.models import DBPost, DBUser

from datetime import datetime
from typing import Optional

from board.rest.models.board import Post, ModifyPostInfo, ResPost
from board.utils.common import make_post_list

router = APIRouter()

# Base.metadata.create_all(engine)


@router.get("/")
def l7ConnectionCheck():
    return "success"


@router.get("/all_post")
def getAllPost(page: Optional[int] = None):
    with MakeSession() as session:
        posts = session.query(DBPost)
        if not page:
            posts = posts.all()
            if posts is None:
                return 'post가 존재하지 않습니다.'

        else:
            offset = (page - 1) * 5
            posts = posts.offset(offset).limit(5).all()
        res = make_post_list(posts, session)
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
