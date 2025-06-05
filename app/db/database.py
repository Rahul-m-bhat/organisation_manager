from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.db.master_db_models import MasterSessionLocal # Import MasterSessionLocal


def get_organization_db_session(db_connection_string: str) -> Generator[Session, None, None]:
    """This function will return a session for a *specific* organization's database"""
    engine = create_engine(db_connection_string)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for master database
def get_master_db() -> Generator[Session, None, None]:
    db = MasterSessionLocal()
    try:
        yield db
    finally:
        db.close()