from fastapi import APIRouter
from board.rest.routers.board import router as post_router
from board.rest.routers.user import router as user_router

routers = APIRouter()
routers.include_router(post_router)
routers.include_router(user_router)