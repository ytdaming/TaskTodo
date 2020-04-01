from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import pymysql
from flask_bootstrap import Bootstrap

app: Flask=Flask(__name__)
app.debug=True
app.config.from_pyfile('../config.py')
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

bootstrap=Bootstrap(app)
db=SQLAlchemy(app)


manager = Manager(app)