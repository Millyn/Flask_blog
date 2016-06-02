# -*- coding=utf-8 -*-
from functools import wraps
from flask import abort
from flask.ext.login import current_user


# # 这里是创建了2个自定义修饰器
# # 如不具备权限均返回403错误页面,所以需要自定义403界面
# def permission_required(permission):
#     """
#     传递一个权限来判断用户是否有权
#     """

#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not current_user.can(permission):
#                 abort(403)
#             return f(*args, **kwargs)

#         return decorated_function

#     return decorator


# def admin_required(f):
#     """
#     判断是否是管理员权限
#     """
#     return permission_required(Permission.ADMINISTER)(f)
