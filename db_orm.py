import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from collections.abc import Generator
load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=5432,
    database="learning_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass

def get_db() -> Generator:
    with SessionLocal() as session:
        yield session
