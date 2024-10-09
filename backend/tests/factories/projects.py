from app.data.models import Project
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory

from tests.conftest import t_test_session, t_test_postgres_dsn

t_dsn = t_test_postgres_dsn()
t_session = t_test_session(t_dsn())


class ProjectFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Project
        sqlalchemy_session = t_session()

    name = "w2e2e2dwpdwpedwnd"


# Example

# session = orm.scoped_session(orm.sessionmaker())
# def build_dsn(**kwargs) -> str:
#    # db_name = "_".join((s.lower() for s in settings.api.title.split(" ")))
#    db_name = "FastApi"
#    test_db_dsn = PostgresDsn.build(
#        scheme=kwargs.get("scheme") or settings.database.scheme,
#        username=kwargs.get("user") or settings.database.user,
#        password=kwargs.get("password") or settings.database.password,
#        host=kwargs.get("host") or settings.database.host,
#        port=kwargs.get("port") or settings.database.port,
#        path=f"/pytest_{db_name}",
#    )
#    return test_db_dsn.unicode_string()
#dsn = build_dsn(scheme="postgresql")
#engine = create_engine(dsn)
#session.configure(bind=engine)
#class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
#    class Meta:
#        model = Project
#        sqlalchemy_session = session