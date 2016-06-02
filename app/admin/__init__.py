# -*- coding=utf-8 -*-
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views, errors

'''
我们需要创建一个新的蓝图模块，名为"admin"
用于我们所有后台功能的模块处理。
'''
