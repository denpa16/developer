## Запросы

### 1. Получение списка объектов
### 2. Получение одного объекта
### 3. Создание объекта
### 4. Удаление объекта
### 5. Создание нескольких объектов одновременно
### 6. Удаление всех объектов
### 7. Обновление нескольких объектов одновременно


```
@router.get("/")
async def get_list(session: AsyncSession = async_session):
    """Список проектов."""
    result = await session.execute(select(Project))
    return result.scalars().all()


@router.get("/{id}")
async def get_one(id: UUID = Path(alias="id"), session: AsyncSession = async_session):
    result = await session.execute(select(Project).where(Project.id == id))
    return result.scalars().one()


@router.get("/bulk_create")
async def bulk_create(session: AsyncSession = async_session):
    """Создание проекта."""
    count = 15
    projects = [
        Project(
            name=f"Project_{i + 1}",
            alias=f"Alias_{i + 1}",
        )
        for i in range(count)
    ]
    session.add_all(projects)
    result = await session.execute(select(Project))
    return result.scalars().all()


@router.get("/delete_all")
async def delete_all(session: AsyncSession = async_session):
    await session.execute(delete(Project))
    result = await session.execute(select(Project))
    return result.scalars().all()

```
