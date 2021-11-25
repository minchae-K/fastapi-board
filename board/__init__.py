from fastapi import FastAPI
from board.rest.routers import board_router

def create_app():
    app = FastAPI()

    app.include_router(board_router)
    return app