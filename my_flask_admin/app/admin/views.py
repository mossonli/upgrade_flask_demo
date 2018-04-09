#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from.import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm
from app.models import Admin, Tag
from functools import wraps
from app import db
import time
current_time = int(time.time())

#admin的登录验证的装饰器
def admin_login_req(func):
    @wraps(func)
    def decorator_func(*args, **kwargs):
        if 'admin'not in session:
            return redirect(url_for("admin.login", next=request.url))
        return func(*args, **kwargs)
    return decorator_func


@admin.route("/")
@admin_login_req
def index():
    return render_template('admin/index.html')


@admin.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter(Admin.name == data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash(u"密码错误！", "err")
            return redirect(url_for('admin.login'))
        session["admin"] = data["account"]
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for("admin.login"))

@admin.route("/modify_pwd/")
@admin_login_req
def modify_pwd():
    return render_template("admin/modify_pwd.html")

# 添加标签
@admin.route("/tag/add/", methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter(Tag.name == data['name']).count()
        if tag == 1:
            flash(u"标签已经存在！", "err")
            return redirect(url_for('admin.tag_add'))
        tag_ = Tag(
            name=data['name'],
            addtime=current_time
        )
        db.session.add(tag_)
        db.session.commit()
        flash(u'添加标签成功', 'ok')
        redirect(url_for('admin.tag_add'))
    return render_template("admin/tag_add.html", form=form)

# 标签的列表页面
@admin.route("/tag/list/<int:page>", methods=['GET', 'POST'])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)

@admin.route("/tag/del/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter(Tag.id == id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash(u"标签删除成功！", "ok")
    return redirect(url_for('admin.tag_list', page=1))

@admin.route("/tag/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    # form.submit.label.text = u"修改"
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter(Tag.name == data['name']).count()
        # if tag.name != data['name'] and 



@admin.route("/movie/add/")
@admin_login_req
def movie_add():
    return render_template("admin/movie_add.html")

@admin.route("/movie/list/")
@admin_login_req
def movie_list():
    return render_template("admin/movie_list.html")

# 上映预告
@admin.route("/preview/add/")
@admin_login_req
def preview_add():
    return render_template("admin/preview_add.html")

@admin.route("/preview/list/")
@admin_login_req
def preview_list():
    return render_template("admin/preview_list.html")

# 会员列表
@admin.route("/user/list/")
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")

# 查看会员
@admin.route("/user/view/")
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")

# 评论列表
@admin.route("/comment/list/")
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")

# 电影收藏列表
@admin.route("/moviecol/list/")
@admin_login_req
def moviecol_list():
    return render_template("admin/moviecol_list.html")

@admin.route("/oplog/list/")
@admin_login_req
def oplog_list():
    return render_template("admin/oplog_list.html")

@admin.route("/adminloginlog/list/")
@admin_login_req
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")

@admin.route("/userloginlog/list/")
@admin_login_req
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")

@admin.route("/role/add/")
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")

@admin.route("/role/list/")
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")

# 权限添加
@admin.route("/auth/add/")
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")

# 权限列表
@admin.route("/auth/list/")
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")

# 添加管理员
@admin.route("/admin/add/")
@admin_login_req
def admin_add():
    return render_template("admin/admin_add.html")

# 管理员列表
@admin.route("/admin/list/")
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")