from fastapi import APIRouter
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.data.models import Building, Floor, Project, Section
from app.dependencies.resourses import async_session

router = APIRouter(prefix="/floors", tags=["Floors"])


@router.get("/")
async def get_list(session: AsyncSession = async_session):
    """Список этажй."""
    floors_query = await session.execute(
        select(
            Floor,
            Section,
            Building,
            Project,
            Section.id.label("section_id"),
            Section.number.label("section_number"),
            Building.id.label("building_id"),
            Building.number.label("building_number"),
            Project.id.label("project_id"),
        )
        .join(Section, Section.id == Floor.section_id)
        .join(Building, Building.id == Section.building_id)
        .join(Project, Project.id == Building.project_id),
    )
    floors = floors_query.fetchall()
    response_data = []
    for floor in floors[:10]:
        floor_data = {
            **{
                column.name: getattr(floor.Floor, column.name)
                for column in floor.Floor.__table__.columns
            },
            **{
                column.name: getattr(floor.Section, column.name)
                for column in floor.Section.__table__.columns
            },
            **{
                column.name: getattr(floor.Building, column.name)
                for column in floor.Building.__table__.columns
            },
            **{
                column.name: getattr(floor.Project, column.name)
                for column in floor.Project.__table__.columns
            },
            "section_number": floor.section_number,
            "building_number": floor.building_number,
            "section_id": floor.section_id,
            "building_id": floor.building_id,
        }
        response_data.append(floor_data)

    return response_data


@router.get("/list")
async def get_another_list(session: AsyncSession = async_session):
    """Список этажй."""
    query = select(Floor).options(
        joinedload(Floor.section).joinedload(Section.building).joinedload(Building.project),
    )

    result = await session.execute(query)
    return result.scalars().all()[:10]


@router.get("/bulk_create")
async def bulk_create(session: AsyncSession = async_session):
    """Создание этажи."""
    sections_query = await session.execute(select(Section))
    sections = sections_query.scalars().all()
    count = 15
    floors = [
        Floor(
            number=i + 1,
            section_id=section.id,
        )
        for i in range(count)
        for section in sections
    ]
    session.add_all(floors)
    result = await session.execute(select(Floor))
    return result.scalars().all()


@router.get("/delete_all")
async def delete_all(session: AsyncSession = async_session):
    """Удалить все этажи."""
    await session.execute(delete(Floor))
    result = await session.execute(select(Floor))
    return result.scalars().all()
