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

@app.route('/login',methods=['POST','GET'])
def login():
    return 'login'

@app.route('/register',methods=['POST','GET'])
def register():
    return 'register'



