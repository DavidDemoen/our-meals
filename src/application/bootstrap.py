import uvicorn

from src.api.app import create_fast_api_app


app = create_fast_api_app()


def run() -> None:
    """Run the application."""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )