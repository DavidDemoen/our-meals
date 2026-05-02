from sqlalchemy import Engine, create_engine

from src.application.core.config import settings

def get_db_engine() -> Engine:
    engine = create_engine(settings.DATABASE_URL, echo=True)
    return engine
