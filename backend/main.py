#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/4/17 17:08
# @Author : zxiaosi
# @desc : main function
import uvicorn
from fastapi import FastAPI

from core import settings
from core.logger import logger
from db import init_db, init_data, init_redis_pool
from register import register_mount, register_exception, register_cors, register_middleware, register_router

app = FastAPI(description=settings.PROJECT_DESC, version=settings.PROJECT_VERSION)


def create_app():
    """ Registration Center """
    register_mount(app)  # Mount static files

    register_exception(app)  # Register to catch global exceptions

    register_router(app)  # register route

    register_middleware(app)  # Registration request response interception

    register_cors(app)  # Register Cross-Origin Request

    logger.info("Log initialization succeeded ！！！")  # Initialize log


@app.on_event("startup")
async def startup():
    create_app()  # Load registry
    # await init_db()  # initialization table
    # await init_data()  # Initialization data
    app.state.redis = await init_redis_pool()  # redis


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()  # close redis


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000)
    # uvicorn.run(app='main:app', host="127.0.0.1", port=8000, debug=True, reload=True)
