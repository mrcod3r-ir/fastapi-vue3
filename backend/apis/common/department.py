#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:18
# @Author : zxiaosi
# @desc : Department table interface
from typing import List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from apis.deps import get_db, get_current_user
from schemas import DepartmentUpdate, DepartmentCreate, DepartmentOut as Department, Result, ResultPlus
from crud import department
from utils import resp_200, IdNotExist

router = APIRouter()


@router.get("/{id}", response_model=Result[Department], summary='Query department information according to id')
async def read_department(id: int, db: AsyncSession = Depends(get_db),
                          user=Security(get_current_user, scopes=[])):
    _department = await department.get(db, id)
    if not _department:
        raise IdNotExist(f"There is no department with id {id} in the system.")
    return resp_200(data=_department, msg=f"The department whose id is {id} was queried.")


@router.get("/", response_model=ResultPlus[Department], summary='Query all departments according to the page number pageIndex and the number of pages per page pageSize')
async def read_departments(pageIndex: int = 1, pageSize: int = 10, db: AsyncSession = Depends(get_db),
                           user=Security(get_current_user, scopes=[])):
    """ Query all departments (pageIndex = -1 && pageSize = -1 means query all) """
    _count = await department.get_number(db)
    _departments = await department.get_multi(db, pageIndex, pageSize)
    return resp_200(data={"count": _count, "list": _departments}, msg=f"Query the information of {pageSize} departments in page {pageIndex}.")


@router.post("/", response_model=Result, summary='Add department information')
async def create_department(department_in: DepartmentCreate, db: AsyncSession = Depends(get_db),
                            user=Security(get_current_user, scopes=["admin"])):
    await department.create(db, obj_in=department_in)
    return resp_200(msg=f"Added the information of the department whose id is {department_in.id}.")


@router.put("/{id}", response_model=Result, summary='Update department information by id')
async def update_department(id: int, department_in: DepartmentUpdate, db: AsyncSession = Depends(get_db),
                            user=Security(get_current_user, scopes=["admin"])):
    rowcount = await department.update(db, id=id, obj_in=department_in)
    if not rowcount: # Every update, the update time of the current data will change, as long as the id exists, it will always return 1
        raise IdNotExist(f"There is no department with id {id} in the system.")
    return resp_200(msg=f"Updated the information of the department whose id is {id}.")


@router.delete("/{id}", response_model=Result, summary='Delete department information by id')
async def delete_department(id: int, db: AsyncSession = Depends(get_db),
                            user=Security(get_current_user, scopes=["admin"])):
    rowcount = await department.remove(db, id)
    if not rowcount:
        raise IdNotExist(err_desc=f"There is no department with id {id} in the system.")
    return resp_200(msg=f'Successfully deleted the information of the department whose id is {id}.')


@router.post("/del/", response_model=Result, summary='Delete information of multiple departments at the same time')
async def delete_departments(idList: List, db: AsyncSession = Depends(get_db),
                             user=Security(get_current_user, scopes=["admin"])):
    rowcount = await department.remove_multi(db, id_list=idList)
    if not rowcount:
        raise IdNotExist(err_desc="The id in the list does not exist in the system.")
    return resp_200(msg='Successfully deleted the information of multiple departments.')


@router.get("/sort/{name}", summary='sort by field')
async def get_select_courses(name: str, pageIndex: int = 1, pageSize: int = 10, db: AsyncSession = Depends(get_db)):
    """ Query all departments (pageIndex = -1 && pageSize = -1 means query all) """
    _count = await department.get_number(db)
    _departments = await department.sort(db, name, pageIndex, pageSize)
    return resp_200(data={"count": _count, "list": _departments}, msg=f"Query the information of {pageSize} departments in page {pageIndex}.")