from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


DATABASE_URL = "sqlite:///./issueflow.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


class Base(DeclarativeBase):
    pass


def get_db():
    with Session(engine) as session:
        yield session