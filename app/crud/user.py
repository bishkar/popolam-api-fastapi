from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseCRUD
from app.models.user import User, UserCreate, UserPreview, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    async def get(self, db_session: AsyncSession) -> UserPreview:
        statement = select(User)
        result = await db_session.execute(statement)
        users = result.scalars().all()
        user_previews = [UserPreview.from_orm(user) for user in users]
        return user_previews

    async def retrieve(
        self, unique_id: int, db_session: AsyncSession
    ) -> Optional[UserPreview]:
        user = await db_session.get(User, unique_id)
        if not user:
            return None

        return UserPreview.from_orm(user)

    async def create(
        self, data: UserCreate, db_session: AsyncSession, is_exist: bool
    ) -> User:
        if is_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username or email already exists",
            )

        user = User(**data.dict())
        user.set_password(data.password)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    async def update(
        self,
        unique_id: int,
        data: UserUpdate,
        db_session: AsyncSession,
        is_exist: bool,
    ) -> Optional[User]:
        if not is_exist:
            raise HTTPException(status_code=404, detail="User not found")

        statement = select(User).where(User.id == unique_id)
        user = await db_session.execute(statement)
        user = user.scalars().first()

        user.is_staff = data.is_staff
        await db_session.commit()

        return HTTPException(status_code=204, detail="User status updated")

    async def delete(
        self, unique_id: int, db_session: AsyncSession, is_exist: bool
    ) -> Optional[User]:
        if not is_exist:
            raise HTTPException(status_code=404, detail="User not found")

        statement = select(User).where(User.id == unique_id)
        user = await db_session.execute(statement)
        user = user.scalars().first()

        if user.on_blacklist:
            raise HTTPException(
                status_code=409, detail="User already on blacklist"
            )

        user.on_blacklist = True
        await db_session.commit()

        return HTTPException(status_code=204, detail="User added to blacklist")
