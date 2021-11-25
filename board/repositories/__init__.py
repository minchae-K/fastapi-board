#DB와 연결을 위해 필요한 것들을 모아둠
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

db_user = 'greenpea'
db_password = ''
db_host = 'localhost'
db_port = '5432'
db_database = 'board'

dsn = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
engine = create_engine(dsn, echo = True)

