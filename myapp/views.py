
from functools import wraps

from myapp import app,db
from flask import render_template, flash, redirect, url_for, session,request
from myapp.models import User,Todo,Category

from myapp.forms import RegisterForm,LoginForm,EditTodoForm,AddToDoForm,AddCategoryForm

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

@app.route('/success')
def success():
    return '<h1>Success</h1>'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def user():
    users=User.query.all()
    print(users)
    # url_for和blueprint: url_for('视图函数')，在蓝图时，url_for('蓝图名.视图函数')
    return redirect(url_for('admin.userlist'))

# 修改用户密码为默认密码
@app.route('/user/resetpasswd/<int:id>')
def resetpasswd(id):
    user = User.query.filter_by(id = id).first()
    passwd=user.username+'123456'
    # if user.verify_password(passwd):
    #
    user.password=passwd
    db.session.add(user)
    db.session.commit()
    flash('修改状态成功')
    print(user)

    return redirect(url_for("admin.userlist"))


@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    # 判断是否是验证提交
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # 1. 判断用户是否存在?
        u = User.query.filter_by(username=username).first()
        if u and u.verify_password(password):
            session['user_id'] = u.id
            session['user'] = u.username
            flash("登录成功!")
            return redirect(url_for('index'))
        else:
            flash("用户名或者密码错误!")
            return redirect(url_for('login'))

    return render_template('wtflogin.html', form=form)

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    # 判断是否是验证提交
    if form.validate_on_submit():
        # 1. 从前端获取用户输入的值;
        email = form.email.data
        username = form.username.data
        password = form.password.data

        # 2. 判断用户是否已经存在? 如果返回位None，说明可以注册;
        u = User.query.filter_by(username=username).first()
        if u:
            flash("用户%s已经存在" % (u.username))
            return redirect(url_for('register'))
        else:
            u = User(username=username, email=email)
            u.password = password
            db.session.add(u)
            db.session.commit()
            flash("注册用户%s成功" % (u.username))
            return redirect(url_for('login'))
    else:
        # 渲染
        return render_template('register.html', form=form)

@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)

    return  redirect(url_for('index'))

# 查看任务
@app.route('/todo/list/')
@app.route('/todo/list/<int:page>')
@is_login
def task_list(page=1):
    if session.get('user'):
        currentuser = session['user']
        user = User.query.filter(User.username == currentuser).first()
        print(user.todos)
        todoPageObj = Todo.query.filter(Todo.user_id == user.id).order_by(Todo.add_time.desc()).paginate(page, per_page=
        app.config['PER_PAGE'])
        todos=todoPageObj.items
        for todo in todos:
            print(todo.user.username)
    else:
        return render_template('index.html')

    return render_template('todo/task_list.html',todoPageObj=todoPageObj)


# 修改任务状态为完成
@app.route('/todo/done/<int:id>/')
def done(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.status=True
    db.session.add(todo)
    db.session.commit()
    flash('修改状态成功')
    print(todo)

    return redirect(url_for("task_list"))


# 修改任务状态为未完成
@app.route('/todo/undo/<int:id>')
def undo(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.status=False
    db.session.add(todo)
    db.session.commit()
    flash('修改状态成功')
    print(todo)

    return redirect(url_for("task_list"))
# 添加任务
@app.route('/todo/add',methods=['GET','POST'])
def task_add():
    form =AddToDoForm()
    if form.validate_on_submit():
        content=form.content.data
        category_id=form.category.data

        print(form.category.data)

        todo=Todo(content=content,category_id=category_id,user_id=session.get('user_id'))
        db.session.add(todo)
        db.session.commit()
        flash('添加任务成功')
        return redirect(url_for('task_list'))
        # pass
    return render_template('todo/task_add.html' , form=form)


# 编辑任务
@app.route('/todo/edit/<int:id>/',methods = ['GET','POST'])
def todo_modify(id):
    form =EditTodoForm()
    todo=Todo.query.filter_by(id=id).first()
    form.content.data=todo.content
    form.category.data=todo.category_id
    if form.validate_on_submit():
        print(request.form)
        content=request.form.get('content')
        category_id=request.form.get("category")
        todo.content=content
        todo.category_id=category_id
        db.session.add(todo)
        db.session.commit()
        flash('更新成功')
        return redirect(url_for('task_list'))


    return render_template('todo/task_edit.html',form = form)


# 删除任务
@app.route('/todo/delete/<int:id>/')
def todo_delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('task_list'))


# 添加任务种类
@app.route('/admin/addcategory',methods=['GET','POST'])
@is_login
@is_admin
def category_add():
    form =AddCategoryForm()
    if form.validate_on_submit():
        name=form.name.data

        category=Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('添加任务成功')
        return redirect(url_for('category_add'))
        # pass
    return render_template('todo/admin_add_category.html' , form=form)
