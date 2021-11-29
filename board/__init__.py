from fastapi import FastAPI
from board.rest.routers import routers

def create_app():
    app = FastAPI()

    app.include_router(routers)
    return app