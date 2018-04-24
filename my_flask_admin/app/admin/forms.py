#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Tag, Auth, Role


class LoginForm(FlaskForm):
    """ 管理员登录表单 """
    account = StringField(
        label=u"账号",
        validators=[
            DataRequired(u"账号不能为空")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入账号！",
            # 注释此处显示forms报错errors信息
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"密码不能为空")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入密码！",
            # 注释此处显示forms报错errors信息
            # "required": "required"
        }
    )
    submit = SubmitField(
        u'登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 验证用户
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter(Admin.name == account).count()
        if admin == 0:
            raise ValidationError(u"账户不存在")        


# 标签验证
class TagForm(FlaskForm):
    name = StringField(
        label=u"名称",
        validators=[
            DataRequired(u"标签名不能为空")
        ],
        description=u"标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": u"请输入标签名称！"
        }
    )
    submit = SubmitField(
        u'添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 电影信息验证
class MovieForm(FlaskForm):
    title = StringField(
        label=u"片名",
        validators=[
            DataRequired(u"片名不能为空！")
        ],
        description=u"片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": u"请输入片名"
        }
    )
    url = FileField(
        label=u"文件",
        validators=[
            DataRequired(u"请上传文件！")
        ],
        description=u"文件",
    )
    info = TextAreaField(
        label=u"简介",
        validators=[
            DataRequired(u"简介不能为空！")
        ],
        description=u"简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    logo = FileField(
        label=u"封面",
        validators=[
            DataRequired(u"请上传封面！")
        ],
        description=u"封面",
    )
    star = SelectField(
        label=u"星级",
        validators=[
            DataRequired(u"请选择星级！")
        ],
        # star的数据类型
        coerce=int,
        choices=[(1, u"1星"), (2, u"2星"), (3, u"3星"), (4, u"4星"), (5, u"5星")],
        description=u"星级",
        render_kw={
            "class": "form-control",
        }
    )
    # 标签要在数据库中查询已存在的标签
    tag_id = SelectField(
        label=u"标签",
        validators=[
            DataRequired(u"请选择标签！")
        ],
        coerce=int,
        # 通过列表生成器生成列表
        choices=[(v.id, v.name) for v in Tag.query.all()],
        description=u"标签",
        render_kw={
            "class": "form-control",
        }
    )
    area = StringField(
        label=u"地区",
        validators=[
            DataRequired(u"请输入地区！")
        ],
        description=u"地区",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入地区！"
        }
    )
    length = StringField(
        label=u"片长",
        validators=[
            DataRequired(u"片长不能为空！")
        ],
        description=u"片长",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入片长！"
        }
    )
    release_time = StringField(
        label=u"上映时间",
        validators=[
            DataRequired(u"上映时间不能为空！")
        ],
        description=u"上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": u"请选择上映时间！",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        u'添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 上映预告表单验证
class PreviewForm(FlaskForm):
    title = StringField(
        label=u"预告标题",
        validators=[
            DataRequired(u"请输入预告标题！")
        ],
        description=u"预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入预告标题！"
        }
    )
    logo = FileField(
        label=u"预告封面",
        validators=[
            DataRequired(u"请上传预告封面！")
        ],
        description=u"预告封面",
    )
    submit = SubmitField(
        label=u'添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label=u"旧密码",
        validators=[
            DataRequired(u"旧密码不能为空！")
        ],
        description=u"旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label=u"新密码",
        validators=[
            DataRequired(u"新密码不能为空！")
        ],
        description=u"新密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入新密码！",
        }
    )
    submit = SubmitField(
        u'编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session['admin']
        admin = Admin.query.filter(Admin.name == name).first()
        if not admin.check_pwd(pwd):
            raise ValidationError(u"就密码错误！")
            

# 权限验证
class AuthForm(FlaskForm):
    name = StringField(
        label=u"权限名称",
        validators=[
            DataRequired(u"权限名称不能为空！")
        ],
        description=u"权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入权限名称！"
        }
    )
    url = StringField(
        label=u"权限地址",
        validators=[
            DataRequired(u"权限地址不能为空！")
        ],
        description=u"权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入权限地址！"
        }
    )
    submit = SubmitField(
        u'编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 角色验证
class RoleForm(FlaskForm):
    name = StringField(
        label=u"角色名称",
        validators=[
            DataRequired(u"角色名称不能为空！")
        ],
        description=u"角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入角色名称！"
        }
    )
    # 多选框 
    auths = SelectMultipleField(
        label=u"权限列表",
        validators=[
            DataRequired("权限列表不能为空！")
        ],
        # 动态数据填充选择栏：列表生成器
        coerce=int,
        choices=[(v.id, v.name) for v in Auth.query.all()],
        description=u"权限列表",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        u'编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 管理员的form验证
class AdminForm(FlaskForm):
    name = StringField(
        label=u"管理员名称",
        validators=[
            DataRequired(u"管理员名称不能为空！")
        ],
        description=u"管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入管理员名称！",
        }
    )
    pwd = PasswordField(
        label=u"管理员密码",
        validators=[
            DataRequired(u"管理员密码不能为空！")
        ],
        description=u"管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入管理员密码！",
        }
    )
    repwd = PasswordField(
        label=u"管理员重复密码",
        validators=[
            DataRequired(u"管理员重复密码不能为空！"),
            EqualTo('pwd', message=u"两次密码不一致！")
        ],
        description=u"管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入管理员重复密码！",
        }
    )
    role_id = SelectField(
        label=u"所属角色",
        coerce=int,
        choices=[(v.id, v.name) for v in Role.query.all()],
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        u'编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )
