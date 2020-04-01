from . import admin
# 导入admin,定义路由时使用


@admin.route('/admin')
def showadmin():
    return 'admin page!'