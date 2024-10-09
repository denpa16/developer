import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
class TestProjects:
    async def test_list(self, api_client: AsyncClient):
        res = await api_client.get("/api/projects/")
        assert res.status_code == 200