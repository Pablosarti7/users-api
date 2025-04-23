from sqlmodel import SQLModel, Session, create_engine
from config import DATABASE_URL
from sqlalchemy import inspect

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    inspector = inspect(engine)
    if not inspector.has_table("user"):
        SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session