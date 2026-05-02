from fastapi import FastAPI

from .routes.main_router import router as api_router


def create_fast_api_app() -> FastAPI:
    app = FastAPI(
            title="Our Meals API",
            version="0.1.0",
        )
    
    app.include_router(api_router, prefix="/api")

    return app
    