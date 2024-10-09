import pytest

from httpx import AsyncClient

from tests.factories.projects import ProjectFactory


@pytest.mark.asyncio
class TestProjects:
    async def test_list(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        await ProjectFactory()
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get("/api/projects/")
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["count"] == 1
