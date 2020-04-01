# admin 目录：包含管理员的业务逻辑的路由和视图
# __init__.py 对Admin业务逻辑程序的初始化操作
# Blueprint 蓝图
from flask import Blueprint

# 蓝图的声明
admin = Blueprint('admin', __name__)
from . import views