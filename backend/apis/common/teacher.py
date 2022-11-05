#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/11/16 9:48
# @Author : zxiaosi
# @desc : Teacher table interface
from typing import List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from apis.deps import get_db, get_current_user
from schemas import TeacherCreate, TeacherUpdate, TeacherOut as Teacher, Result, ResultPlus
from crud import teacher
from utils import resp_200, IdNotExist

router = APIRouter()


@router.get("/{id}", response_model=Result[Teacher], summary='Query teacher information according to id')
async def read_teacher(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=[])):
    _teacher = await teacher.get(db, id)
    if not _teacher:
        raise IdNotExist(err_desc=f"The teacher with id {id} does not exist in the system.")
    return resp_200(data=_teacher, msg=f"The teacher whose id is {id} is queried.")


@router.get("/", response_model=ResultPlus[Teacher], summary='Query all teachers according to the page number pageIndex and the number of pages per page pageSize')
async def read_teachers(pageIndex: int = 1, pageSize: int = 10, db: AsyncSession = Depends(get_db),
                        user=Security(get_current_user, scopes=[])):
    """ Query all teachers (pageIndex = -1 && pageSize = -1 means query all) """
    _count = await teacher.get_number(db)
    _teachers = await teacher.get_multi(db, pageIndex, pageSize)
    return resp_200(data={"count": _count, "list": _teachers}, msg=f"Query the information of {pageSize} teachers in page {pageIndex}.")


@router.post("/", response_model=Result, summary='Add teacher information')
async def create_teacher(teacher_in: TeacherCreate, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=['admin'])):
    await teacher.create(db, obj_in=teacher_in)
    return resp_200(msg=f"Added teacher information with id {teacher_in.id}.")


@router.put("/{id}", response_model=Result, summary='Update teacher information by id')
async def update_teacher(id: int, teacher_in: TeacherUpdate, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=['admin'])):
    rowcount = await teacher.update(db, id=id, obj_in=teacher_in)
    if not rowcount:
        raise IdNotExist(err_desc=f"The teacher with id {id} does not exist in the system.")
    return resp_200(msg=f"Updated teacher information with id {id}.")


@router.delete("/{id}", response_model=Result, summary='Delete teacher information by id')
async def delete_teacher(id: int, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=['admin'])):
    rowcount = await teacher.remove(db, id)
    if not rowcount:
        raise IdNotExist(err_desc=f"The teacher with id {id} does not exist in the system.")
    return resp_200(msg=f"Deleted teacher information with id {id}.")


@router.post("/del/", response_model=Result, summary='Delete multiple teacher information at the same time')
async def delete_teachers(idList: List, db: AsyncSession = Depends(get_db),
                          user=Security(get_current_user, scopes=['admin'])):
    rowcount = await teacher.remove_multi(db, id_list=idList)
    if not rowcount:
        raise IdNotExist(err_desc="The id in the list does not exist in the system.")
    return resp_200(msg='Successfully deleted multiple teacher information.')