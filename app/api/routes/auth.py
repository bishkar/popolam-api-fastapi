from fastapi import APIRouter, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.future import select
from typing import Annotated, Union

from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.misc import get_token_for_user, verify_token
from app.misc.jwt_helpers import create_token_pair
from app.models import User
from app.models.token import TokenPair
from app.models.user import UserLogin, UserPreview


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/")
async def get_token(
    data: UserLogin,
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> TokenPair:
    statement = select(User).where(User.username == data.username)
    user = await db_session.execute(statement)
    user = user.scalars().first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")
    return await get_token_for_user(user, data.password)

@router.get("/users/me/")
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> UserPreview:
    payload = await verify_token(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=403, detail="Invalid token payload")
    
    statement = select(User).where(User.id == user_id)
    user = await db_session.execute(statement)
    user = user.scalars().first()
    
    return UserPreview.from_orm(user)

@router.post("/refresh/")
async def refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> TokenPair:
    payload = await verify_token(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=403, detail="Invalid token payload")
    
    user = await db_session.get(User, user_id)

    return await create_token_pair(user)
