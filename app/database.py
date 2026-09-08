from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session

from app.config import settings


connect_args = {}

if settings.database_url.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    settings.database_url,
    connect_args=connect_args
)


if settings.database_url.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(
        dbapi_connection,
        connection_record
    ):
        cursor = dbapi_connection.cursor()
        cursor.execute(
            "PRAGMA foreign_keys=ON"
        )
        cursor.close()


class Base(DeclarativeBase):
    pass


def get_db():
    with Session(engine) as session:
        yield session