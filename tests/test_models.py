from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

pymysql.install_as_MySQLdb()

app=Flask(__name__)
app.debug=True
app.config.from_pyfile('../config.py')
# app.config
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(30), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now()) # 账户创建时间
    # 1).  User添加属性todos; 2). Todo添加属性user;
    todos = db.relationship('Todo', backref="user")
    categories = db.relationship('Category', backref='user')

    @property
    def password(self):
        """u.password"""
        raise  AttributeError("密码属性不可以读取")


    def __repr__(self):
        return  "<User %s>" %(self.username)

# 任务和分类的关系： 一对多
# 分类是一， 任务是多, 外键写在多的一端
class Todo(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.String(100)) # 任务内容
    status = db.Column(db.Boolean, default=False) # 任务的状态
    add_time = db.Column(db.DateTime, default=datetime.now())  # 任务创建时间
    # 任务的类型,关联另外一个表的id
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 任务所属用户;
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return  "<Todo %s>" %(self.content[:6])


class Category(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now())  # 任务创建时间
    # 1). Category添加一个属性todos, 2). Todo添加属性category；
    todos = db.relationship('Todo', backref='category')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return  "<Category %s>" %(self.name)


user=User.query.filter_by(username='admin').first()
print(user.todos)

todo=Todo.query.filter_by(id='1').first()
print(todo.user)
#
# if __name__ =='__main__':
#     app.run()