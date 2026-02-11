import pytest
from startup.database import Base, engine, SessionLocal


@pytest.fixture(scope="session")
def db_engine():

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(db_engine):
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
