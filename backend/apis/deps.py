#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/15 20:10
# @Author : zxiaosi
# @desc : dependencies
from typing import AsyncGenerator

from fastapi import Depends, Security, HTTPException
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core import check_jwt_token, settings
from db import async_session, MyRedis
from schemas import TokenData
from utils import UserNotExist, PermissionNotEnough
from utils.permission_assign import by_scopes_get_crud, handle_oauth2_scopes

get_token = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login", scopes=handle_oauth2_scopes())


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """ sql connection session """
    async with async_session() as session:
        yield session


async def get_redis(request: Request) -> MyRedis:
    """ redis connection object """
    return await request.app.state.redis


async def get_current_user(
        security_scopes: SecurityScopes,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(get_token)
):
    """ Get the current user (docs interface documentation) """
    payload = await check_jwt_token(token) # Check if the token has expired
    token_scopes = payload.get("scopes", []) # No value, return []
    token_data = TokenData(scopes=token_scopes, sub=payload.get("sub")) # User permissions for token storage
    crud_obj = by_scopes_get_crud(token_scopes) # Verify user exists
    user = await crud_obj.get(db, id=payload.get("sub"))
    if not user:
        raise UserNotExist()
    for scope in security_scopes.scopes: # Checked user permissions
        if scope not in token_data.scopes:
            raise PermissionNotEnough('Insufficient permission, access denied')
    return user

# def get_current_active_user(current_user: Admin = Security(get_current_user, scopes=["admin"])):
# """ Get the current logged in user """
# if not admin.is_active_def(current_user):
# raise HTTPException(status_code=400, detail="User is not logged in!!!")
# return current_user