#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/1/17 15:15
# @Author : zxiaosi
# @desc : Home
import json
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from db import MyRedis
from apis.deps import get_redis
from schemas import Todo, TodoId
from utils import resp_200

router = APIRouter()


@router.get("/dashboard", response_class=ORJSONResponse, summary='Visits && To-dos && Requests && To-dos')
async def get_visit_todo_request(redis: MyRedis = Depends(get_redis)):
    """ Query homepage data (visits && to-do items && requests && to-do items) """
    visit_num = await redis.get('visit_num')
    todo_num = await redis.llen('todo_list')
    request_num = await redis.get('request_num')
    todo_list = await redis.list_loads('todo_list', 6)
    data = {'visit_num': visit_num, 'todo_num': todo_num, 'request_num': request_num, 'todo_list': todo_list}
    return resp_200(data=data, msg='queried traffic && to-do items && number of requests && to-do items')


@router.post("/todo/add", summary='Add todo')
async def add_todo(todo_in: Todo, redis: MyRedis = Depends(get_redis)):
    """ Add To Do """
    text = {'title': todo_in.title, 'status': todo_in.status}
    await redis.cus_lpush('todo_list', text)
    return resp_200(msg='Add to-do success!')


@router.post("/todo/update", response_class=ORJSONResponse, summary='Update todo according to index')
async def update_todo(todo_in: TodoId, redis: MyRedis = Depends(get_redis)):
    """ Update To Do """
    obj = await redis.get_list_by_index('todo_list', todo_in.id)
    obj["status"] = bool(1 - obj["status"]) # negate noqa
    await redis.lset('todo_list', todo_in.id, json.dumps(obj))
    return resp_200(msg='Update to-do success!')