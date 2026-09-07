from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# SQLite database file
DATABASE_PATH = PROJECT_ROOT / "data" / "candidate_risk.db"

# SQLAlchemy database URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


# Database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base class for database models
Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()