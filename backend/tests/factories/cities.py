import factory

from app.data.models import City
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory

from tests.conftest import get_factory_session


class CityFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = City
        sqlalchemy_session = get_factory_session()

    name = factory.Sequence(lambda n: f"name_{n}")
    alias = factory.Sequence(lambda n: f"alias_{n}")

