from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app import settings
from app.api.routes import router as api_router
from app.core.lifecycle import lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_STR}/openapi.json",
        lifespan=lifespan,
        debug=settings.DEBUG,
        middleware=[
            Middleware(
                GZipMiddleware,
                minimum_size=1024,  # 1KB
            ),
        ],
    )

    if settings.FRONTEND_URL:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.FRONTEND_URL,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/", tags=["root"])
    async def read_root():
        return {
            "name": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "debug": settings.DEBUG,
            "host": settings.HOST,
            "port": settings.PORT,
        }

    app.include_router(api_router, prefix=settings.API_STR)
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

    return app


app = create_app()
