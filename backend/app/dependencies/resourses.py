from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.sqlalchemy_session import get_db_session

async_session: AsyncSession = Depends(get_db_session)
