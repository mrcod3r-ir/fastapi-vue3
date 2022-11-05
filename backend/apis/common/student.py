#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/11/17 11:12
# @Author : zxiaosi
# @desc : Student table interface
from typing import List
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from apis.deps import get_db, get_current_user
from schemas import StudentCreate, StudentUpdate, StudentOut as Student, Result, ResultPlus
from crud import student
from utils import resp_200, IdNotExist

router = APIRouter()


@router.get("/{id}", response_model=Result[Student], summary='Query student information based on id')
async def read_student(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=[])):
    _student = await student.get(db, id)
    if not _student:
        raise IdNotExist(err_desc=f"There is no student with id {id} in the system.")
    return resp_200(data=_student, msg=f"The student whose id is {id} is queried.")


@router.get("/", response_model=ResultPlus[Student], summary='Query all students according to the page number pageIndex and the number of pages per page pageSize')
async def read_students(pageIndex: int = 1, pageSize: int = 10, db: AsyncSession = Depends(get_db),
                        user=Security(get_current_user, scopes=[])):
    """ Query all departments (pageIndex = -1 && pageSize = -1 means query all) """
    _count = await student.get_number(db)
    _students = await student.get_multi(db, pageIndex, pageSize)
    return resp_200(data={"count": _count, "list": _students}, msg=f"Query the information of {pageSize} students in page {pageIndex}.")


@router.post("/", response_model=Result, summary='Add student information')
async def create_student(student_in: StudentCreate, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=['admin'])):
    await student.create(db, obj_in=student_in)
    return resp_200(msg=f"Added student information with id {student_in.id}.")


@router.put("/{id}", response_model=Result, summary='Update student information by id')
async def update_student(id: int, student_in: StudentUpdate, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=['admin'])):
    rowcount = await student.update(db, id=id, obj_in=student_in)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no student with id {id} in the system.")
    return resp_200(msg=f"Updated the information of the student whose id is {id}.")


@router.delete("/{id}", response_model=Result, summary='Delete student information by id')
async def delete_student(id: int, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=['admin'])):
    rowcount = await student.remove(db, id)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no student with id {id} in the system.")
    return resp_200(msg=f"Deleted student information with id {id}.")


@router.post("/del/", response_model=Result, summary='Delete multiple student information at the same time')
async def delete_students(idList: List, db: AsyncSession = Depends(get_db),
                          user=Security(get_current_user, scopes=['admin'])):
    rowcount = await student.remove_multi(db, id_list=idList)
    if not rowcount:
        raise IdNotExist(err_desc="The id in the list does not exist in the system.")
    return resp_200(msg='Successfully deleted multiple student information.')


# @router.get("/detail/{id}", summary='Get detailed information')
# async def get_detail(id: int, db: AsyncSession = Depends(get_db)):
# _data = await student.get_detail(db, id)
# return _data