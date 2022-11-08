import os

import pytest as pytest
import sqlalchemy as sa
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database

from app.helper.db import db_session
from app.model import Category
from app.model.base import Base
from main import app

load_dotenv(dotenv_path='./.env', verbose=True)
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# This fixture is the main difference to before. It creates a nested
# transaction, recreates it when the applications code calls session.commit
# and rolls it back at the end.
@pytest.fixture(autouse=True, scope='function')
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()
    Category.create(db=session, data={"id": 1, "name_vi": "Đại số", "name_en": "Math", "parent_id": None})
    Category.create(db=session, data={"id": 2, "name_vi": "Cơ sở dữ liệu", "name_en": "Database", "parent_id": None})
    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override as before, it uses the one provided by the
# session fixture.
@pytest.fixture(autouse=True, scope='function')
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[db_session] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[db_session]


# A fixture for create database and clean up database before and after all tests
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    if database_exists(SQLALCHEMY_DATABASE_URI):
        drop_database(SQLALCHEMY_DATABASE_URI)
    create_database(SQLALCHEMY_DATABASE_URI)  # Create the test database.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield  # Run the tests.
    drop_database(SQLALCHEMY_DATABASE_URI)  # Drop the test database