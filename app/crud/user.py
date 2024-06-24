from typing import Optional, List

from fastapi import Depends
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseCRUD
from app.dependencies.db import get_db
from app.models.user import User, UserCreate, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    def __init__(self, db_session: AsyncSession = Depends(get_db)):
        self.db_session = db_session

    # add crud methods