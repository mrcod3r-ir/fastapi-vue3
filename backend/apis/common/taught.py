#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/5/10 21:08
# @Author : zxiaosi
# @desc : teach table interface
from typing import List
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from apis.deps import get_db, get_current_user
from models import Teacher
from schemas import TaughtCreate, TaughtUpdate, TaughtOut as Taught, Result, ResultPlus
from crud import taught
from utils import resp_200, IdNotExist

router = APIRouter()


@router.get("/{id}", response_model=Result[Taught], summary='Query teaching information according to id')
async def read_taught(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=[])):
    _taught = await taught.get(db, id)
    if not _taught:
        raise IdNotExist(err_desc=f"There is no lecture with id {id} in the system.")
    return resp_200(data=_taught, msg=f"The lecture with the id of {id} was queried.")


@router.get("/", response_model=ResultPlus[Taught], summary='Query all lectures according to the page number pageIndex and the number of pages per page pageSize')
async def read_taughts(pageIndex: int = 1, pageSize: int = 10, db: AsyncSession = Depends(get_db),
                       user=Security(get_current_user, scopes=[])):
    """ Query all departments (pageIndex = -1 && pageSize = -1 means query all) """
    _count = await taught.get_number(db)
    _taughts = await taught.get_multi(db, pageIndex, pageSize)
    return resp_200(data={"count": _count, "list": _taughts}, msg=f"Query the {pageSize} lecture information in page {pageIndex}.")


@router.post("/", response_model=Result, summary='Add lecture information')
async def create_taught(taught_in: TaughtCreate, db: AsyncSession = Depends(get_db),
                        user=Security(get_current_user, scopes=['admin'])):
    await taught.create(db, obj_in=taught_in)
    return resp_200(msg="Added lecture information.")


@router.put("/{id}", response_model=Result, summary='Update lecture information by id')
async def update_taught(id: int, taught_in: TaughtUpdate, db: AsyncSession = Depends(get_db),
                        user=Security(get_current_user, scopes=['admin'])):
    rowcount = await taught.update(db, id=id, obj_in=taught_in)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no lecture with id {id} in the system.")
    return resp_200(msg=f"Updated lecture information with id {id}.")


@router.delete("/{id}", response_model=Result, summary='Delete lecture information by id')
async def delete_taught(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=['admin'])):
    rowcount = await taught.remove(db, id)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no lecture with id {id} in the system.")
    return resp_200(msg=f"Deleted lecture information with id {id}.")


@router.post("/del/", response_model=Result, summary='Delete multiple lecture information at the same time')
async def delete_taughts(idList: List, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=['admin'])):
    rowcount = await taught.remove_multi(db, id_list=idList)
    if not rowcount:
        raise IdNotExist(err_desc="The id in the list does not exist in the system.")
    return resp_200(msg='Successfully deleted multiple lecture information.')


@router.get("/detail/", response_model=Result, summary='Get the details of the teacher's lecture information')
async def get_course_detail(db: AsyncSession = Depends(get_db), user: Teacher = Security(get_current_user, scopes=[])):
    data = await taught.get_course(db, id=user.id)
    return resp_200(data=data, msg='Get the details of the teacher's lecture.')