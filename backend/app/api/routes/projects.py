from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
async def get_list() -> list:
    """Список проектов."""
    return []
