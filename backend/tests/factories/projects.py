import factory

from app.data.models import Project
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory

from tests.conftest import get_factory_session


class ProjectFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Project
        sqlalchemy_session = get_factory_session()

    name = factory.Sequence(lambda n: f"name_{n}")
