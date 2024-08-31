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


    subquery_building_count = (
        select(
            Building.project_id,
            func.count(Building.id).label("building_count"),
        )
        .group_by(Building.project_id)
        .subquery()
    )
    subquery_section_count = (
        select(
            Project.id.label("project_id"),
            func.count(Section.id).label("section_count"),
        )
        .join(Building, Building.project_id == Project.id)
        .join(Section, Section.building_id == Building.id)
        .group_by(Project.id)
        .subquery()
    )
    result = await session.execute(
        select(
            Project.id,
            Project.name,
            Project.alias,
            func.coalesce(subquery_building_count.c.building_count, 0).label("building_count"),
            func.coalesce(subquery_section_count.c.section_count, 0).label("section_count"),
        )
        .outerjoin(subquery_building_count, subquery_building_count.c.project_id == Project.id)
        .outerjoin(subquery_section_count, subquery_section_count.c.project_id == Project.id),
    )
    return [
        {
            "id": str(proj.id),
            "name": proj.name,
            "alias": proj.alias,
            "building_count": proj.building_count,
            "section_count": proj.section_count,
        }
        for proj in result
    ]

```
