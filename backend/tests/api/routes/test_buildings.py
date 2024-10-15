import pytest

from httpx import AsyncClient

from tests.factories.projects import ProjectFactory, BuildingFactory


@pytest.mark.asyncio
class TestBuildings:
    async def test_list(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        projects_count = 5
        projects = [await ProjectFactory() for _ in range(projects_count)]
        buildings = [await BuildingFactory() for project in projects]
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get("/api/buildings/")
        assert response.status_code == 200
        res_json = response.json()
