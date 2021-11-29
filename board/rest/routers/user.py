from fastapi import APIRouter

from board.repositories.models import DBUser
from board.rest.models.board import User, ModifyUserInfo
from board.rest.routers.board import MakeSession

router = APIRouter()

@router.get("/user_info/{user_id}")
def getUserInfo(user_id: int):
    with MakeSession() as session:
        user = session.query(DBUser).filter_by(id=user_id).first()

        res = User(name=user.name, email=user.email, password=user.password)

        return res

@router.post("/join_user")
def joinUser(user: User):
    # Base.metadata.create_all(engine)

    with MakeSession() as session:
        new_user = DBUser()
        new_user.name = user.name
        new_user.email = user.email
        new_user.password = user.password

        session.add(new_user)
        session.commit()

        result = session.query(DBUser).last()
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


@router.put("/inactivate_user")
def inactivateUser(user_id: int):
    #user를 비활성화
    with MakeSession() as session:
        user = session.query(DBUser).filter_by(id=user_id).first()

        user.inactivate = True

        session.add(user)
        session.commit()
    return user