import pytest

from httpx import AsyncClient

from tests.factories.projects import ProjectFactory
from tests.factories.cities import CityFactory


@pytest.mark.asyncio
class TestProjects:
    """Тесты проектов."""

    async def test_list(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        """Тест списка проектов."""
        projects_count = 5
        city = await CityFactory()
        projects = [await ProjectFactory(city_id=city.id) for _ in range(projects_count)]
        url = "/api/projects/"
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get(url)
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["count"] == projects_count
        assert res_json["results"][0]["id"] == str(projects[0].id)
        assert res_json["results"][0]["name"] == projects[0].name
        assert res_json["results"][0]["alias"] == projects[0].alias

    async def test_retrieve(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        """Тест получения проекта."""
        projects_count = 5
        city = await CityFactory()
        projects = [await ProjectFactory(city_id=city.id) for _ in range(projects_count)]
        [await ProjectFactory() for _ in range(projects_count)]
        url = f"/api/projects/{projects[0].alias}/"
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get(url)
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["id"] == str(projects[0].id)
        assert res_json["name"] == projects[0].name
        assert res_json["alias"] == projects[0].alias

    async def test_genplan_action(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        """Тест получения генплана проекта."""
        projects_count = 5
        city = await CityFactory()
        projects = [await ProjectFactory(city_id=city.id) for _ in range(projects_count)]
        [await ProjectFactory() for _ in range(projects_count)]
        url = f"/api/projects/{projects[0].alias}/genplan/"
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get(url)
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["id"] == str(projects[0].id)
        assert res_json["name"] == projects[0].name
        assert res_json["alias"] == projects[0].alias

    async def test_facets(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        """Тест фасетов проектов."""
        projects_count = 5
        city = await CityFactory()
        projects = [await ProjectFactory(city_id=city.id) for _ in range(projects_count)]
        url = "/api/projects/facets/"
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get(url)
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["count"] == projects_count
        facets = res_json["facets"]
        for facet in facets:
            if facet["name"] == "alias":
                for project in projects:
                    assert project.alias in facet["choices"]

    async def test_specs(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        """Тест фасетов проектов."""
        projects_count = 5
        city = await CityFactory()
        projects = [await ProjectFactory(city_id=city.id) for _ in range(projects_count)]
        url = "/api/projects/specs/"
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get(url)
        assert response.status_code == 200
        specs = response.json()
        specs_names = ["alias", "city"]
        for spec in specs:
            assert spec["name"] in specs_names
            if spec["name"] == "alias":
                assert len(spec["choices"]) == projects_count
                for project in projects:
                    assert {
                               "label": str(project.id),
                               "value": project.alias,
                           } in spec["choices"]


    async def test_alias_filter(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        """Тест фильтра проектов по алиасу."""
        projects_count = 5
        city = await CityFactory()
        projects = [await ProjectFactory(city_id=city.id) for _ in range(projects_count)]
        url = f"/api/projects/?alias={projects[0].alias}"
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get(url)
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["count"] == 1
        assert res_json["results"][0]["id"] == str(projects[0].id)
        assert res_json["results"][0]["name"] == projects[0].name
        assert res_json["results"][0]["alias"] == projects[0].alias

    async def test_city_filter(self, api_client: AsyncClient, sqlalchemy_assert_max_num_queries):
        """Тест фильтра проектов по городу."""
        city_count = 3
        cities = [await CityFactory() for _ in range(city_count)]
        projects_count = 5
        projects = [
            await ProjectFactory(city_id=city.id)
            for _ in range(projects_count)
            for city in cities
        ]
        url = f"/api/projects/?city={cities[0].alias}"
        with sqlalchemy_assert_max_num_queries(1):
            response = await api_client.get(url)
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["count"] == projects_count
        assert res_json["results"][0]["id"] == str(projects[0].id)
        assert res_json["results"][0]["name"] == projects[0].name
        assert res_json["results"][0]["alias"] == projects[0].alias
