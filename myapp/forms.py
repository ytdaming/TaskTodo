from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError,SelectField,DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# 注册表单
from myapp.models import User,Category


class RegisterForm(FlaskForm):
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired(message=u"用户名不能为空"),
            Email(),
        ],
        render_kw = {'placeholder': u'输入EMAIL地址'}

    )
    username = StringField(
        label="用户名",
        validators=[
            DataRequired(message=u'用户名不能为空'),
            Length(3,10,message=u'用户名应为3~20位之间'),
        ],
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired(),
            Length(6, 12, "密码必须是6-12位")
        ]
    )

    repassword = PasswordField(
        label='确认密码',
        validators=[
            EqualTo("password", "密码与确认密码不一致")
        ]
    )

    submit = SubmitField(
        label="注册"
    )

    # *****************************************************
    # 默认情况下validate_username会验证用户名是否正确， 验证的规则， 写在函数里面
    def validate_username(self, field):
        # filed.data ==== username表单提交的内容
        u = User.query.filter_by(username=field.data).first()
        if u:
            raise ValidationError("用户名%s已经注册" % (u.username))

    def validate_email(self, filed):
        u = User.query.filter_by(email=filed.data).first()
        if u:
            raise ValidationError("邮箱%s已经注册" % (u.email))


# 登录表单
class LoginForm(FlaskForm):
    username = StringField(
        label="用户名",
        validators=[
            DataRequired(),
            Length(3, 12, "用户名必须是3-12位")

        ],
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired(),
            Length(6, 12, "密码必须是6-12位")
        ]
    )
    submit = SubmitField(
        label="登录"
    )

class AddToDoForm(FlaskForm):
    content=StringField(
        label='任务内容',
        validators=[DataRequired()]
    )
    category=SelectField(
        label='任务类型',
        coerce=int,
        choices=[(item.id,item.name) for item in Category.query.all()]
    )
    submit=SubmitField(
        label='添加任务',
    )


# 关于任务的基类
class TodoForm(FlaskForm):
    content = StringField(
        label="任务内容",
        validators=[
            DataRequired()
        ]
    )
    # 任务类型
    category = SelectField(
        label="任务类型",
        coerce=int,
        choices=[(item.id, item.name) for item in Category.query.all()]
    )
class AddTodoForm(TodoForm):
    finish_time = DateTimeField(
        label="任务终止日期"
    )
    submit = SubmitField(
        label="添加任务",
    )

class EditTodoForm(TodoForm):
    submit = SubmitField(
        label="编辑任务",
    )


class AddCategoryForm(FlaskForm):
    name=StringField(
        label="类型名",
        validators=[
            DataRequired(),
            Length(3, 12, "任务类型名必须是3-12位")
        ]
    )
    submit=SubmitField(
            label="编辑任务",
    )
    def validate_categoryname(self, field):
        # filed.data ==== username表单提交的内容
        category_name = Category.query.filter_by(name=field.data).first()
        if category_name:
            raise ValidationError("用户名%s已经注册" % (category_name.name))