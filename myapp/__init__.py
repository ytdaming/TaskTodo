from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import pymysql
from flask_bootstrap import Bootstrap

pymysql.install_as_MySQLdb()

app: Flask=Flask(__name__)
app.debug=True


db=SQLAlchemy(app)


from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

bootstrap=Bootstrap(app)
app.config.from_pyfile('../config.py')


manager = Manager(app)