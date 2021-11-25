from fastapi import APIRouter

from board.rest.routers.board import router

board_router = APIRouter()

board_router.include_router(router)