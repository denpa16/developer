from contextlib import contextmanager

import pytest
from typing import AsyncGenerator, Callable
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import PostgresDsn
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.sqlalchemy_session import AsyncSessionBuilder
from sqlalchemy_utils import create_database, drop_database

from app.config import settings
from app.data.models import Base

@pytest.fixture()
def test_session(test_postgres_dsn) -> AsyncSession:
    test_db_dsn = test_postgres_dsn(scheme=settings.database.scheme)
    async_session_builder = AsyncSessionBuilder(database_url=test_db_dsn, echo=settings.database.echo)
    yield async_session_builder()


@pytest.fixture(scope="session")
def test_postgres_dsn() -> Callable:
    def build_dsn(**kwargs) -> str:
        #db_name = "_".join((s.lower() for s in settings.api.title.split(" ")))
        db_name = "FastApi"
        test_db_dsn = PostgresDsn.build(
            scheme=kwargs.get("scheme") or settings.database.scheme,
            username=kwargs.get("user") or settings.database.user,
            password=kwargs.get("password") or settings.database.password,
            host=kwargs.get("host") or settings.database.host,
            port=kwargs.get("port") or settings.database.port,
            path=f"/pytest_{db_name}",
        )
        return test_db_dsn.unicode_string()

    return build_dsn

@pytest.fixture(scope="session")
def create_db(test_postgres_dsn):
    dsn: str = test_postgres_dsn(scheme="postgresql")
    try:
        create_database(dsn)
        yield
    finally:
        drop_database(dsn)


@pytest.fixture()
def tables(create_db, test_postgres_dsn):
    dsn: str = test_postgres_dsn(scheme="postgresql")
    engine = create_engine(dsn, echo=False)
    Base.metadata.create_all(engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture()
async def override_get_db_session(tables, test_session) -> AsyncGenerator:
    async def get_db():
        async with test_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()

    return get_db


@pytest.fixture()
def app(override_get_db_session) -> FastAPI:
    from app import app
    from app.data.sqlalchemy_session import get_db_session

    app.dependency_overrides[get_db_session] = override_get_db_session
    yield app



@pytest.fixture()
async def api_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


class EvenNumberChecker:
    def __init__(
            self,
            reference_count: int,
            # result_count: int
    ):
        self.reference_count = reference_count
        print(self.reference_count)
        # self.result_count = result_count

    def __enter__(self):
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

@pytest.fixture()
def sqlalchemy_assert_max_num_queries(test_session):
    @contextmanager
    def check_max_count_database_queries(ref_count):
        queries = []
        t_session = test_session()
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            queries.append(statement)
        event.listen(t_session.sync_session.bind.engine, "before_cursor_execute", before_cursor_execute)
        try:
            assert len(queries) <= ref_count
            yield queries
        except AssertionError:
            msg = f"Database expected max num {ref_count} queries, but {len(queries)} queries were done"
            raise AssertionError(msg)
        event.remove(t_session.sync_session.bind.engine, "before_cursor_execute", before_cursor_execute)
    return check_max_count_database_queries


@pytest.fixture()
def sqlalchemy_assert_num_queries(test_session):
    @contextmanager
    def check_count_database_queries(ref_count):
        queries = []
        t_session = test_session()
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            queries.append(statement)
        event.listen(t_session.sync_session.bind.engine, "before_cursor_execute", before_cursor_execute)
        try:
            assert len(queries) <= ref_count
            yield queries
        except AssertionError:
            msg = f"Database expected max num {ref_count} queries, but {len(queries)} queries were done"
            raise AssertionError(msg)
        event.remove(t_session.sync_session.bind.engine, "before_cursor_execute", before_cursor_execute)
    return check_count_database_queries