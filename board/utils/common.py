from typing import List

from board.repositories.models import DBPost, DBUser
from board.rest.models.board import ResPost

from board.repositories import MakeSession


def make_post_list(posts: List[DBPost], session: MakeSession):
    res = []
    for post in posts:
        name = session.query(DBUser.name).filter_by(id=post.user_id).first()
        modify = False if post.created_at.strftime("%m/%d/%Y, %H:%M:%S") == post.updated_at.strftime(
            "%m/%d/%Y, %H:%M:%S") else True
        res.append(ResPost(user_name=name[0], title=post.title, content=post.content, modified=modify))
    return res