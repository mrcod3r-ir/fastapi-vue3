#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/11/18 10:25
# @Author : zxiaosi
# @desc : Course selection interface
from typing import List
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from apis.deps import get_db, get_current_user
from models import Student
from schemas import ElectiveCreate, ElectiveUpdate, ElectiveOut as Elective, Result, ResultPlus
from crud import elective
from utils import resp_200, IdNotExist

router = APIRouter()


@router.get("/{id}", response_model=Result[Elective], summary='Query course selection information according to id')
async def read_elective(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=[])):
    _elective = await elective.get(db, id)
    if not _elective:
        raise IdNotExist(err_desc=f"There is no course with id {id} in the system.")
    return resp_200(data=_elective, msg=f"The elective course with the id of {id} was queried.")


@router.get("/", response_model=ResultPlus[Elective], summary='Query all elective courses according to the page number pageIndex and the number of pages per page pageSize')
async def read_electives(pageIndex: int = 1, pageSize: int = 10, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=[])):
    """ Query all departments (pageIndex = -1 && pageSize = -1 means query all) """
    _count = await elective.get_number(db)
    _electives = await elective.get_multi(db, pageIndex, pageSize)
    return resp_200(data={"count": _count, "list": _electives}, msg=f"Query the {pageSize} elective information on page {pageIndex}.")


@router.post("/", response_model=Result, summary='Add course selection information')
async def create_elective(elective_in: ElectiveCreate, db: AsyncSession = Depends(get_db),
                          user=Security(get_current_user, scopes=[])):
    await elective.create(db, obj_in=elective_in)
    return resp_200(msg='Added course selection information.')


@router.put("/{id}", response_model=Result, summary='Update course selection information by id')
async def update_elective(id: int, elective_in: ElectiveUpdate, db: AsyncSession = Depends(get_db),
                          user=Security(get_current_user, scopes=[])):
    rowcount = await elective.update(db, id=id, obj_in=elective_in)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no course with id {id} in the system.")
    return resp_200(msg=f"Updated the course selection information with id {id}.")


@router.delete("/{id}", response_model=Result, summary='Delete course selection information by id')
async def delete_elective(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=[])):
    rowcount = await elective.remove(db, id)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no course with id {id} in the system.")
    return resp_200(msg=f"Deleted course selection information with id {id}.")


@router.post("/del/", response_model=Result, summary='Delete multiple course selection information at the same time')
async def delete_electives(idList: List, db: AsyncSession = Depends(get_db),
                           user=Security(get_current_user, scopes=[])):
    rowcount = await elective.remove_multi(db, id_list=idList)
    if not rowcount:
        raise IdNotExist(err_desc="The id in the list does not exist in the system.")
    return resp_200(msg='Successfully deleted multiple course selection information.')


@router.post("/add/{courseId}", response_model=Result, summary='Add course selection information')
async def create_elective_by_course_id(courseId: int, db: AsyncSession = Depends(get_db),
                                       user: Student = Security(get_current_user, scopes=[])):
    obj = await elective.is_exist(db, courseId=courseId, studentId=user.id)
    if obj:
        data, msg = 0, 'Data already exists.'
    else:
        data, msg = 1, 'Added course selection information.'
        await elective.create(db, obj_in={'grade': 0, 'studentId': user.id, 'courseId': courseId})
    return resp_200(data=data, msg=msg)


@router.post("/del/{courseId}", response_model=Result, summary='Delete course selection information through other fields')
async def del_elective_by_filed(courseId: int, db: AsyncSession = Depends(get_db),
                                user: Student = Security(get_current_user, scopes=[])):
    obj = await elective.is_exist(db, courseId=courseId, studentId=user.id)
    if obj:
        data, msg = 1, 'The data exists, the withdrawal is successful'
        rowcount = await elective.remove(db, id=obj.id)
        if not rowcount:
            raise IdNotExist(err_desc=f"There is no course with id {id} in the system.")
    else:
        data, msg = 0, 'Data does not exist, failed to drop the class! '
    return resp_200(data=data, msg=msg)


@router.get("/detail/", response_model=Result, summary='Get the details of the student's course selection information')
async def get_course_detail(db: AsyncSession = Depends(get_db), user: Student = Security(get_current_user, scopes=[])):
    data = await elective.get_course(db, id=user.id)
    return resp_200(data=data, msg='Get the details of the student's course selection information.')