#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/11/17 16:42
# @Author : zxiaosi
# @desc : Curriculum interface
from typing import List
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from apis.deps import get_db, get_current_user
from schemas import CourseCreate, CourseUpdate, CourseOut as Course, Result, ResultPlus
from crud import course
from utils import resp_200, IdNotExist

router = APIRouter()


@router.get("/{id}", response_model=Result[Course], summary='Query course information according to id')
async def read_course(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=[])):
    _course = await course.get(db, id)
    if not _course:
        raise IdNotExist(err_desc=f"The course with id {id} does not exist in the system.")
    return resp_200(data=_course, msg=f"The course whose id is {id} is queried.")


@router.get("/", response_model=ResultPlus[Course], summary='Query all courses according to the page number pageIndex and the number of pages per page pageSize')
async def read_courses(pageIndex: int = 1, pageSize: int = 10, db: AsyncSession = Depends(get_db),
                       user=Security(get_current_user, scopes=[])):
    """ Query all departments (pageIndex = -1 && pageSize = -1 means query all) """
    _count = await course.get_number(db)
    _courses = await courses.get_multi(db, pageIndex, pageSize)
    return resp_200(data={"count": _count, "list": _courses}, msg=f"Query the {pageSize} course information in page {pageIndex}.")


@router.post("/", response_model=Result, summary='Add course information')
async def create_course(course_in: CourseCreate, db: AsyncSession = Depends(get_db),
                        user=Security(get_current_user, scopes=["admin"])):
    await course.create(db, obj_in=course_in)
    return resp_200(msg=f"Added course information with id {course_in.id}.")


@router.put("/{id}", response_model=Result, summary='Update course information by id')
async def update_course(id: int, course_in: CourseUpdate, db: AsyncSession = Depends(get_db),
                        user=Security(get_current_user, scopes=["admin"])):
    rowcount = await course.update(db, id=id, obj_in=course_in)
    if not rowcount:
        raise IdNotExist(err_desc=f"The course with id {id} does not exist in the system.")
    return resp_200(msg=f"Updated course information with id {id}.")


@router.delete("/{id}", response_model=Result, summary='Delete course information by id')
async def delete_course(id: int, db: AsyncSession = Depends(get_db), user=Security(get_current_user, scopes=["admin"])):
    rowcount = await course.remove(db, id)
    if not rowcount:
        raise IdNotExist(err_desc=f"The course with id {id} does not exist in the system.")
    return resp_200(msg=f"Deleted course information with id {id}.")


@router.post("/del/", response_model=Result, summary='Delete multiple course information at the same time')
async def delete_courses(idList: List, db: AsyncSession = Depends(get_db),
                         user=Security(get_current_user, scopes=["admin"])):
    rowcount = await course.remove_multi(db, id_list=idList)
    if not rowcount:
        raise IdNotExist(err_desc="The id in the list does not exist in the system.")
    return resp_200(msg='Successfully deleted multiple course information.')