#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError
from app.models import User


class RegistForm(FlaskForm):
    name = StringField(
        label=u"昵称",
        validators=[
            DataRequired(u"昵称不能为空！")
        ],
        description=u"昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入昵称！",
        }
    )
    email = StringField(
        label=u"邮箱",
        validators=[
            DataRequired(u"邮箱不能为空！"),
            Email(u"邮箱格式不正确！")
        ],
        description=u"邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入邮箱！",
        }
    )
    phone = StringField(
        label=u"手机",
        validators=[
            DataRequired(u"手机号不能为空！"),
            Regexp("1[3458]\\d{9}", message=u"手机格式不正确！")
        ],
        description=u"手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入手机！",
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"密码不能为空！")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入密码！",
        }
    )
    repwd = PasswordField(
        label=u"确认密码",
        validators=[
            DataRequired(u"请输入确认密码！"),
            EqualTo('pwd', message=u"两次密码不一致！")
        ],
        description=u"确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入确认密码！",
        }
    )
    submit = SubmitField(
        u'注册',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter(User.name == name).count()
        if user == 1:
            raise ValidationError(u"名称已经存在")

    def validate_eamil(self, field):
        email = field.data
        email_info = User.query.filter(User.email == email).count()
        if email_info == 1:
            raise ValidationError(u"邮箱已经被注册")
    
    def validate_phone(self, field):
        phone = field.data
        phone_info = User.query.filter(User.phone == phone).count()
        if phone_info == 1:
            raise ValidationError(u"手机号已经被占用")


class LoginForm(FlaskForm):
    name = StringField(
        label=u"账号",
        validators=[
            DataRequired(u"账号不能为空！")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入账号！",
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"密码不能为空！")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入密码！",
        }
    )
    submit = SubmitField(
        u'登录',
        render_kw={
            "class": "btn btn-lg btn-primary btn-block",
        }
    )

    def validate_name(self, field):
        name = field.data
        user_obj = User.query.filter_by(name=name).count()
        if user_obj == 0:
            raise ValidationError("账号不存在! ")


class UserdetailForm(FlaskForm):
    name = StringField(
        label=u"账号",
        validators=[
            DataRequired(u"账号不能为空！")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入账号！",
        }
    )
    email = StringField(
        label=u"邮箱",
        validators=[
            DataRequired(u"邮箱不能为空！"),
            Email(u"邮箱格式不正确！")
        ],
        description=u"邮箱",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱！",
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired(u"手机号不能为空！"),
            Regexp("1[3458]\\d{9}", message="手机格式不正确！")
        ],
        description=u"手机",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入手机！",
        }
    )
    face = FileField(
        label=u"头像",
        validators=[
            DataRequired(u"请上传头像！")
        ],
        description=u"头像",
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
    submit = SubmitField(
        u'保存修改',
        render_kw={
            "class": "btn btn-success",
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
            DataRequired(u"新密码不能为空！"),
        ],
        description=u"新密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入新密码！",
        }
    )
    submit = SubmitField(
        u'修改密码',
        render_kw={
            "class": "btn btn-success",
        }
    )


class CommentForm(FlaskForm):
    content = TextAreaField(
        label=u"内容",
        validators=[
            DataRequired(u"请输入内容！"),
        ],
        description=u"内容",
        render_kw={
            "id": "input_content"
        }
    )
    submit = SubmitField(
        u'提交评论',
        render_kw={
            "class": "btn btn-success",
            "id": "btn-sub"
        }
    )