#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/11/8 10:44
# @Author : zxiaosi
# @desc : log
import os

from loguru import logger

from core import settings
from utils import create_dir


# Create log file name
def logger_file() -> str:
    """ Create log file name """
    log_path = create_dir(settings.LOGGER_DIR)

    """ Keep the maximum number of logs in the folder (for local debugging)
    Local debugging requires multiple restarts, and log rotation will not take effect """
    file_list = os.listdir(log_path)
    if len(file_list) > 3:
        os.remove(os.path.join(log_path, file_list[0]))

    # log output path
    return os.path.join(log_path, settings.LOGGER_NAME)


# see details : https://loguru.readthedocs.io/en/stable/overview.html#features
logger.add(
    logger_file(),
    encoding=settings.GLOBAL_ENCODING,
    level=settings.LOGGER_LEVEL,
    rotation=settings.LOGGER_ROTATION,
    retention=settings.LOGGER_RETENTION,
    enqueue=True
)
