#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/12/28 19:16
# @Author : zxiaosi
# @desc : login
import json
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from core import settings, create_access_token
from db import MyRedis
from models import Admin, Teacher, Student
from schemas import Result, Token, AdminOut, TeacherOut, StudentOut
from apis.deps import get_redis, get_db, get_current_user
from utils import resp_200, SetRedis, ErrorUser, by_ip_get_address
from utils.permission_assign import by_scopes_get_crud

router = APIRouter()


# User login is recommended to take a look at this library: https://fastapi-users.github.io/fastapi-users/
# The login here uses OAuth2, and the JWT used for storage has nothing to do with the token stored in redis (the front-end request needs to send a form request)
# The token expiration time in OAuth2 is related to the set time and the opening and closing of the service. When the time expires or the service is closed, the token expires
@router.post("/login", response_model=Token, summary="docs interface documentation login && login interface")
async def login_access_token(
        request: Request,
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """ OAuth2 compatible token login, obtain access token for request of interface document """
    crud_obj = by_scopes_get_crud(form_data.scopes) # Permission assignment
    _user = await crud_obj.authenticate(db, username=form_data.username, password=form_data.password)
    if not _user:
        raise ErrorUser()

    address = by_ip_get_address(request.client.host) # Get the address according to ip
    await crud_obj.update(db, id=_user.id, obj_in={'address': address})

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": str(_user.id), "scopes": form_data.scopes}, access_token_expires)

    try:
        await request.app.state.redis.incr('visit_num') # User visits increase by 1
        await request.app.state.redis.set(token, json.dumps(jsonable_encoder(_user)), access_token_expires)
    except Exception as e:
        raise SetRedis(f'Redis failed to store token!--{e}')

    # Here 'access_token' and 'token_type' must be written, otherwise the get_current_user dependency cannot get the token
    # Fields can be added (modify the Token return model in schemas/token first)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/admin/index", response_model=Result[AdminOut], summary="Get current administrator")
def get_current_admin(current_user: Admin = Security(get_current_user, scopes=["admin"])):
    return resp_200(data=jsonable_encoder(current_user), msg='Get current administrator information!')


@router.get("/teacher/index", response_model=Result[TeacherOut], summary="Get current teacher")
def get_current_teacher(current_user: Teacher = Security(get_current_user, scopes=["teacher"])):
    return resp_200(data=jsonable_encoder(current_user), msg='Get current teacher information!')


@router.get("/student/index", response_model=Result[StudentOut], summary="Get current student")
def get_current_student(current_user: Student = Security(get_current_user, scopes=["student"])):
    return resp_200(data=jsonable_encoder(current_user), msg='Get current student information!')


@router.post("/logout", response_model=Result, summary="Logout (hidden)", include_in_schema=False)
async def logout_token(request: Request, redis: MyRedis = Depends(get_redis)):
    if 'authorization' in request.headers.keys():
        token = request.headers.get('authorization')[7:] # Remove the Bearer in front of the token
        await redis.delete(token)
    return resp_200(msg='Logout')