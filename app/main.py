from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.base import api_router
from app.database import async_session, engine


def build_app() -> FastAPI:
    application = FastAPI(title="App", debug=True, version="1.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router)
    return application


app = build_app()


# @app.on_event("startup")
# async def startup():
#     app.state.DB = async_session

# @app.on_event("shutdown")
# async def shutdown():
#     await engine.dispose()
