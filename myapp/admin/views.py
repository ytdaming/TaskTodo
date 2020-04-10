from functools import wraps

from . import admin
# from ..views import is_login,is_admin
# from myapp import db
from myapp.models import User,Category
# from myapp.forms import AddCategoryForm
from flask import render_template, session, flash, redirect, url_for


# 导入admin,定义路由时使用


def is_login(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if session.get('user',None):
            return f(*args,**kwargs)
        else:
            flash('用户必须登录才能访问%s！'%(f.__name__))
            return redirect(url_for('login'))
    return wrapper

def is_admin(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if session.get('user',None)=='root':
            return f(*args,**kwargs)
        else:
            flash('只有管理员root才能访问%s'%(f.__name__))
            return redirect(url_for('login'))
    return wrapper

@admin.route('/admin')
@is_login
@is_admin
def showadmin():
    return 'admin page!'


#查看用户列表
@admin.route('/admin/userlist')
@is_login
@is_admin
# def userlist():
#     return 'userlist'
def userlist():
    users=User.query.all()
    print(users)
    for user in users:
        print(user.username)
        print(user.email)
    return render_template('userlist.html',users=users)


# 添加任务各类
