import pytest

from httpx import AsyncClient

from tests.factories.projects import ProjectFactory


@pytest.mark.asyncio
class TestProjects:
    async def test_list(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        projects_count = 5
        projects = [await ProjectFactory() for _ in range(projects_count)]
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get("/api/projects/")
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["count"] == projects_count
        assert res_json["results"][0]["id"] == str(projects[0].id)

    async def test_list_s(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        projects_count = 5
        projects = [await ProjectFactory() for _ in range(projects_count)]
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get("/api/projects/")
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["count"] == projects_count
        assert res_json["results"][0]["id"] == str(projects[0].id)

    async def test_list_ss(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        projects_count = 5
        projects = [await ProjectFactory() for _ in range(projects_count)]
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get("/api/projects/")
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["count"] == projects_count
        assert res_json["results"][0]["id"] == str(projects[0].id)
