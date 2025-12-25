from fastapi import FastAPI

from app.interfaces.api.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="rewise_neet_server", version="0.1.0")
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
