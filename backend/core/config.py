#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 17:02
# @Author : zxiaosi
# @desc : configuration file
import secrets
from typing import Union, List
from pydantic import BaseSettings, AnyHttpUrl

project_desc = """
    🎉 Admin Interface Summary 🎉
    ✨ Account: admin ✨
    ✨ Password: 123456 ✨
    ✨ Scopes: admin ✨
"""


class Settings(BaseSettings):
    PROJECT_DESC: str = project_desc # description
    PROJECT_VERSION: Union[int, str] = 5.0 # version
    BASE_URL: AnyHttpUrl = "http://127.0.0.1:8000" # Development environment

    API_PREFIX: str = "/api" # interface prefix
    STATIC_DIR: str = 'static' # static file directory
    GLOBAL_ENCODING: str = 'utf-8' # global encoding
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000", "http://8.136.82.204:8001"] # Cross-domain request

    SECRET_KEY: str = secrets.token_urlsafe(32) # Key (the key will change every time the service is restarted, and the token will expire due to failure of decryption, which can be set as a constant)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1 # token expiration time: 60 minutes * 24 hours * 1 days = 1 days

    REDIS_URI: str = "redis://:123456@localhost:6379/1" # redis
    # DATABASE_URI: str = "sqlite+aiosqlite:///./sql_app.db?check_same_thread=False" # Sqlite (asynchronous)
    DATABASE_URI: str = "mysql+asyncmy://root:123456@localhost:3306/elective_system?charset=utf8" # MySQL (asynchronous)
    # DATABASE_URI: str = "postgresql+asyncpg://postgres:123456@localhost:5432/postgres" # PostgreSQL (async)
    DATABASE_ECHO: bool = False # Whether to print the database log (you can see the information of table creation, table data addition, deletion, modification and query)

    LOGGER_DIR: str = "logs" # log folder name
    LOGGER_NAME: str = '{time:YYYY-MM-DD_HH-mm-ss}.log' # log file name (time format)
    LOGGER_LEVEL: str = 'DEBUG' # log level: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "12:00" # Log fragmentation: Split logs by time period/file size. For example ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "7 days" # Log retention time: beyond will delete the oldest log. For example ["1 days"]

    # permission data table (must be in the format {'name', 'description'})
    PERMISSION_DATA: List[dict] = [{'admin': 'Administrator'}, {'teacher': 'Teacher'}, {'student': 'Student'}]

    class Config:
        case_sensitive = True # case sensitive


settings = Settings()