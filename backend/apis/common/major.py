#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/11/1 21:17
# @Author : zxiaosi
# @desc : Professional table interface
from typing import List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from apis.deps import get_db, get_current_user
from schemas import MajorCreate, MajorUpdate, MajorOut as Major, Result, ResultPlus
from crud import major
from utils import resp_200, IdNotExist

router = APIRouter()


@router.get("/{id}", response_model=Result[Major], summary='Query professional information according to id')
async def read_major(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=[])):
    _major = await major.get(db, id)
    if not _major:
        raise IdNotExist(f"The profession with id {id} does not exist in the system.")
    return resp_200(data=_major, msg=f"The major whose id is {id} is queried.")


@router.get("/", response_model=ResultPlus[Major], summary='Query all majors according to the page number pageIndex and the number of pages per page pageSize')
async def read_majors(pageIndex: int = 1, pageSize: int = 10, db: AsyncSession = Depends(get_db),
                      user=Security(get_current_user, scopes=[])):
    """ Query all majors (pageIndex = -1 && pageSize = -1 means query all) """
    _count = await major.get_number(db)
    _majors = await major.get_multi(db, pageIndex, pageSize)
    return resp_200(data={"count": _count, "list": _majors}, msg=f"Query the {pageSize} professional information in page {pageIndex}.")


@router.post("/", response_model=Result, summary='Add professional information')
async def create_major(major_in: MajorCreate, db: AsyncSession = Depends(get_db),
                       user=Security(get_current_user, scopes=["admin"])):
    await major.create(db, obj_in=major_in)
    return resp_200(msg=f"Added professional information with id {major_in.id}.")


@router.put("/{id}", response_model=Result, summary='Update professional information by id')
async def update_major(id: int, major_in: MajorUpdate, db: AsyncSession = Depends(get_db),
                       user=Security(get_current_user, scopes=["admin"])):
    rowcount = await major.update(db, id=id, obj_in=major_in)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no major with id {id} in the system.")
    return resp_200(msg=f"Updated professional information with id {id}.")


@router.delete("/{id}", response_model=Result, summary='Delete professional information by id')
async def delete_major(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=["admin"])):
    rowcount = await major.remove(db, id)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no major with id {id} in the system.")
    return resp_200(msg=f"Deleted professional information with id {id}.")


@router.post("/del/", response_model=Result, summary='Delete multiple professional information at the same time')
async def delete_majors(idList: List, db: AsyncSession = Depends(get_db),
                        user=Security(get_current_user, scopes=["admin"])):
    rowcount = await major.remove_multi(db, id_list=idList)
    if not rowcount:
        raise IdNotExist(err_desc="The id in the list does not exist in the system.")
    return resp_200(msg='Delete multiple professional information at the same time.')