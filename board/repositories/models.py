from sqlalchemy import Column, Integer, String
from board.repositories import Base

class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)