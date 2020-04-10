SQLALCHEMY_DATABASE_URI='mysql://admin:123456@192.168.19.128/tasktodo'
#配置使用的数据库URL，配置MySQL的URL格式
# SQLALCHEMY_DATABASE_URI=r'sqlite:///data.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# """如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这
# 需要额外的内存， 如果不必要的可以禁用它。""""

#flask-form组件功能设置，入境问俗csrf加密功能

CSRF_ENABLED = True
SECRET_KEY = '123456'


PER_PAGE=5