from typing import Optional, List

from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from app.crud.base import BaseCRUD
from app.dependencies.db import get_db
from app.models.user import User, UserCreate, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    async def get(self, db_session: AsyncSession) -> List[User]:
        statement = select(User)
        result = await db_session.execute(statement)
        return result.scalars().all()
    
    async def retrieve(self, unique_id: int, db_session: AsyncSession) -> Optional[User]:        
        statement = select(User).where(User.id == unique_id)
        result = await db_session.execute(statement)
        return result.scalars().first()
    
    async def create(self, data: UserCreate, db_session: AsyncSession, is_exist: bool) -> User:
        if is_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail="User with this username or email already exists")
        
        user = User(**data.dict())
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user
    
    async def update(self, unique_id: int, data: UserUpdate, db_session: AsyncSession) -> Optional[User]:
        return HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
    
    async def delete(self, unique_id: int, db_session: AsyncSession, is_exist: bool) -> Optional[User]:
        if not is_exist:
            raise HTTPException(status_code=404, detail="User not found")
        statement = delete(User).where(User.id == unique_id)
        result = await db_session.execute(statement)
        await db_session.commit()
        return HTTPException(status_code=204, detail="User deleted")
    