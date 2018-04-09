#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin

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