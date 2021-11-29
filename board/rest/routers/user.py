from fastapi import APIRouter

from board.repositories.models import DBUser
from board.rest.models.board import User, ModifyUserInfo
from board.rest.routers.board import MakeSession

router = APIRouter()

@router.get("/user_info/{user_id}")
def getUserInfo(user_id: int):
    with MakeSession() as session:
        user = session.query(DBUser).filter_by(id=user_id, inactivate=False).first()
        print('user : {}'.format(user))

        if user is None:
            return '등록되지 않은 사용자이거나 탈퇴한 사용자입니다.'
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

        result = session.query(DBUser.name).filter_by(name=user.name).first()
    return '{}님 계정이 등록되었습니다.'.format(result[0])


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
    return '데이터 수정이 완료되었습니다.'


@router.put("/inactivate_user")
def inactivateUser(user_id: int):
    #user를 비활성화
    with MakeSession() as session:
        user = session.query(DBUser).filter_by(id=user_id).first()
        name = user.name

        user.inactivate = True

        session.add(user)
        session.commit()
    return '{}님의 계정이 비활성화되었습니다.'.format(name)