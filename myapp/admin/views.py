from . import admin
from myapp.models import User
from flask import render_template

# 导入admin,定义路由时使用


@admin.route('/admin')
def showadmin():
    return 'admin page!'


#查看用户列表
@admin.route('/admin/userlist')
# def userlist():
#     return 'userlist'
def userlist():
    users=User.query.all()
    print(users)
    for user in users:
        print(user.username)
        print(user.email)
    return render_template('userlist.html',users=users)