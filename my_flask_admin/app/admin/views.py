#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from.import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from app.models import Admin, Tag, Movie, Preview, User, Comment
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
from app import db, app
import time
from app.utils.page import Pagination

import uuid
import os
current_time = int(time.time())

#admin的登录验证的装饰器
def admin_login_req(func):
    @wraps(func)
    def decorator_func(*args, **kwargs):
        if 'admin'not in session:
            return redirect(url_for("admin.login", next=request.url))
        return func(*args, **kwargs)
    return decorator_func



# 修改文件名
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


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
    form.submit.label.text = u"修改"
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter(Tag.name == data['name']).count()
        if tag.name != data['name'] and tag_count == 1:
            flash(u"标签已经存在！", "err")
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        tag.addtime = current_time
        db.session.add(tag)
        db.session.commit()
        flash(u"标签修改成功！", "ok")
        redirect(url_for('admin.tag_edit', id=tag.id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


@admin.route("/movie/add/", methods=['GET', 'POST'])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length'],
            addtime=current_time
        )
        db.session.add(movie)
        db.session.commit()
        flash(u"电影添加成功！", "ok")
        return redirect(url_for('admin.movie_add'))
    return render_template("admin/movie_add.html", form=form)

@admin.route("/movie/list/<int:page>", methods=["GET"])
@admin_login_req
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag, Movie.tag_id == Tag.id).order_by(Movie.addtime.desc()).add_entity(Tag).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)

@admin.route("/movie/del/<int:id>", methods=["GET"])
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash(u"电影删除成功！", "ok")
    return redirect(url_for('admin.movie_list', page=1))


@admin.route("/movie/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))
    form.submit.label.text = u"修改"
    # 因为是编辑，所以非空验证空
    # 编辑页面的时候要对页面进行复初值，(前端操作、后端操作)
    if request.method == 'GET':
        form.info.data = movie.info
        form.star.data = movie.star
        form.tag_id.data = movie.tag_id
        form.release_time.data = movie.release_time
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter(Movie.title == data["title"]).count()
        # 存在一个相同名字的电影，有可能是他自己， 也可能重名， 如果现在的movie不等于要提交数据中的title，说明有两个
        if movie_count == 1 and movie.title != data['title']:
            flash(u"片名已经存在", "err")
            return redirect(url_for('admin.movie_edit', id=id))
        # 创建目录
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        # 上传视频
        if form.url.data.filename != "":
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)
        # 上传图片
        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + movie.logo)


        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie.info = data["info"]
        movie.title = data["title"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        # movie.url = movie.url
        db.session.add(movie)
        db.session.commit()
        flash(u"修改电影信息成功", "ok")
        return redirect(url_for('admin.movie_edit', id=id))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


# 上映预告
@admin.route("/preview/add/", methods=['GET', 'POST'])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        preview = Preview(
                title=data["title"],
                logo=logo,
                addtime=current_time
            )
        db.session.add(preview)
        db.session.commit()
        flash(u"添加预告成功！", "ok")
        return redirect(url_for('admin.preview_add'))
    return render_template("admin/preview_add.html", form=form)

@admin.route("/preview/list/<int:page>",  methods=['GET', 'POST'])
@admin_login_req
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=2)
    return render_template("admin/preview_list.html", page_data=page_data)

# 删除预告
@admin.route("/preview/del/<int:id>/", methods=["GET"])
@admin_login_req
def preview_del(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash(u"删除预告成功！", "ok")
    return redirect(url_for('admin.preview_list', page=1))

@admin.route('/preview/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def preview_edit(id=None):
    form = PreviewForm()
    form.logo.validators = []
    form.submit.label.text = u"修改"
    preview = Preview.query.get_or_404(int(id))
    if request.method == 'GET':
        form.title.data = preview.title
    if form.validate_on_submit():
        data = form.data
        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + preview.logo)
        preview.title = data["title"]
        db.session.add(preview)
        db.session.commit()
        flash("修改预告成功！", "ok")
        return redirect(url_for('admin.preview_edit', id=id))
    return render_template("admin/preview_edit.html", form=form, preview=preview)

# 会员列表
@admin.route("/user/list/<int:page>")
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)

# 查看会员
@admin.route("/user/view/<int:id>")
@admin_login_req
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user)

# 会员删除
@admin.route("/user/del/<int:id>/", methods=["GET"])
@admin_login_req
def user_del(id=None):
    # 因为删除当前页。假如是最后一页，这一页已经不见了。回不到。
    # from_page = int(request.args.get('fp')) - 1
    # 此处考虑全删完了，没法前挪的情况，0被视为false
    # if not from_page:
    #     from_page = 1
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash(u"删除会员成功！", "ok")
    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route("/comment/list/<int:page>")
@admin_login_req
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie, Comment.movie_id == Movie.id).add_entity(Movie).join(User, Comment.user_id == User.id).add_entity(User).paginate(page=page, per_page=10)
    return render_template("admin/comment_list.html", page_data=page_data)

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