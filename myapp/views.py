from myapp import app,db
from flask import render_template, flash, redirect, url_for, session,request
from myapp.models import User,Todo,Category
from myapp.forms import RegisterForm,LoginForm

@app.route('/baselogin',methods=['POST','GET'])
def baselogin():
    form = LoginForm()
    # 判断是否是验证提交
    if form.validate_on_submit():
        # 跳转
        flash(form.username.data + '|' + form.password.data)
        return redirect(url_for('success'))
    else:
        # 渲染
        return render_template('wtflogin.html', form=form)


@app.route('/success')
def success():
    return '<h1>Success</h1>'

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






