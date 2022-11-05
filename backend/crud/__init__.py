#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/14 16:59
# @Author : zxiaosi
# @desc : Add, delete, modify and check operations of the database (dao layer)
from .base import ModelType, CRUDBase
from .department import department
from .major import major
from .teacher import teacher
from .student import student
from .course import course
from .elective import elective
from .taught import taught
from .admin import admin