from myapp import app,db
from flask import render_template, flash, redirect, url_for, session,request
from myapp.models import User,Todo,Category


@app.route('/')
def index():
    return 'index'


@app.route('/user')
def user():
    users=User.query.all()
    print(users)
    return 'users'