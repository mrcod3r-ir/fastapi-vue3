#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/1/5 13:55
# @Author : zxiaosi
# @desc : check redis
from fastapi import APIRouter, Depends

from db import MyRedis
from apis.deps import get_redis

router = APIRouter()


@router.get("/health-check")
async def health_check(redis: MyRedis = Depends(get_redis)):
    try:
        # key:test:keys => key/test/keys
        value = await redis.get('request_num')
        msg = "Open Redis successfully! ! !"
    except Exception as e:  # noqa: E722
        value = 0
        msg = f"Sorry, can't open Redis!!! {e}"
    return {"request": f"total number of requests {value}", "msg": msg}
