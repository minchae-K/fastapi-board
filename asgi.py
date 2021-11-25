import uvicorn

from board import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app)
    # uvicorn.run(app, host = "127.0.0.1", port = "8000") 등으로 설정 가능