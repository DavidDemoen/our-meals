from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/meals")
def list_meals() -> list[dict[Any, Any]]:
    return [
        {"id": 1, "name": "Pasta"},
        {"id": 2, "name": "Pizza"},
    ]