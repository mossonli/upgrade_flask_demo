#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from.import home
from flask import render_template, redirect, url_for, flash, session, request, Response
from app.home.forms import RegistForm, LoginForm, UserdetailForm, PwdForm, CommentForm
from app.models import User, UserLog, Preview, Tag, Movie, Comment, MovieCol
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask.ext.redis import FlaskRedis
import time
import uuid
import os
import datetime
from app import db, app, rd
from functools import wraps
from sqlalchemy import and_
import json
current_time = int(time.time())


# 登录的装饰器
def user_login_req(func):
    @wraps(func)
    def decorator_func(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return func(*args, **kwargs)
    return decorator_func


def change_filename(filename):
    """
    修改文件名称
    """
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + \
               str(uuid.uuid4().hex) + fileinfo[-1]
    return filename



@home.route("/<int:page>/", methods=['GET'])
@home.route("/", methods=["GET"])
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query
    # 标签
    tid = request.args.get("tid", 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    #星级
    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    # 时间
    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    # 播放量
    pm = request.args.get("pm", 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )
    # 评论量
    cm = request.args.get("cm", 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=10)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    return render_template("home/index.html", tags=tags, p=p, page_data=page_data)

@home.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        userobj = User.query.filter(User.name == data['name']).first_or_404()
        # 密码错误时 check_pwd返回flase， 此时not check_pwd(data['name'])
        if not userobj.check_pwd(data["pwd"]):
            flash(u"密码不正确", "err")
            return redirect(url_for("home.login"))
        session["user"] = userobj.name
        session["user_id"] = userobj.id
        userlog = UserLog(
            user_id=userobj.id,
            ip=request.remote_addr,
            addtime=current_time
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user_info"))
    return render_template("home/login.html", form=form)

@home.route("/logout/")
@user_login_req
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))

@home.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid.uuid4().hex,
            addtime=current_time
        
        )
        db.session.add(user)
        db.session.commit()
        flash(u"注册成功", "ok")
    return render_template("home/register.html", form=form)

# 会员中心 修改会员资料
@home.route("/user_info/", methods=['GET', 'POST'])
@user_login_req
def user_info():
    form = UserdetailForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET": # 赋初值
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if form.face.data != "":
            file_face = secure_filename(form.face.data.filename)
            if not os.path.exists(app.config["FC_DIR"]):
                os.makedirs(app.config["FC_DIR"])
                os.chmod(app.config["FC_DIR"], 'rw')
            user.face = change_filename(file_face)
            form.face.data.save(app.config["FC_DIR"] + user.face)

        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在!", "err")
            return redirect(url_for("home.user"))

        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已经存在!", "err")
            return redirect(url_for("home.user"))

        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("手机已经存在!", "err")
            return redirect(url_for("home.user"))

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash(u"修改成功", "ok")
        return redirect(url_for('home.user_info'))
    return render_template("home/user_info.html", form=form, user=user)

@home.route("/modify_pwd/", methods=['GET', 'POST'])
@user_login_req
def modify_pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter(User.name == session["user"]).first()
        if not user.check_pwd(data["old_pwd"]):
            flash(u"旧密码错误", "err")
            return redirect(url_for("home.modify_pwd"))
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash(u"修改密码成功", "ok")
        return redirect(url_for("home.logout"))
    return render_template("home/modify_pwd.html", form=form)

@home.route("/comments/<int:page>/")
@user_login_req
def comments(page=None):
    if page is None:
        page = 1
    print(session['user_id'])
    
    p = Comment.query.join(Movie, Comment.movie_id == Movie.id).add_entity(Movie).join(User, session['user_id'] == User.id).add_entity(User).order_by(Comment.addtime.desc())
    print(p)
    # page_data = Comment.query.join(Movie, Comment.movie_id == Movie.id).add_entity(Movie).join(User, session['user_id'] == User.id).add_entity(User).order_by(Comment.addtime.desc()).paginate(page=page, per_page=10)
    # page_data = User.query.join(Movie, User.id == session['user_id']).add_entity(User).join(Comment, Movie.id == Comment.movie_id).add_entity(Comment).order_by(Comment.addtime.desc()).paginate(page=page, per_page=10)
    page_data = Comment.query.join(Movie, Comment.movie_id == Movie.id).add_entity(Movie).join(User, session['user_id'] == User.id).add_entity(User).paginate(page=page, per_page=10)
    
    return render_template("home/comments.html", page_data=page_data)

@home.route("/loginlog/<int:page>/")
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = UserLog.query.filter(UserLog.user_id == int(session["user_id"])).order_by(UserLog.addtime.desc()).paginate(page=page, per_page=2)
    return render_template("home/loginlog.html", page_data=page_data)


# 添加电影收藏
@home.route("/moviecol/add/", methods=['GET', 'POST'])
@user_login_req
def moviecol_add():
    uid = request.args.get("uid", "")
    mid = request.args.get("mid", "")
    print(uid, mid, '2222222222')
    moviecol = MovieCol.query.filter(and_(MovieCol.user_id == int(uid), MovieCol.movie_id == int(mid))).count()
    # 已经添加了收藏
    if moviecol == 1:
        data = dict(ok=0)
    if moviecol == 0:
        movie_col = MovieCol(user_id=int(uid), movie_id=int(mid), addtime=current_time)
        db.session.add(movie_col)
        db.session.commit()
        data = dict(ok=1)
    return json.dumps(data)

# 电影收藏
@home.route("/moviecol/<int:page>/", methods=['GET', 'POST'])
@user_login_req
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = MovieCol.query.join(Movie, MovieCol.movie_id == Movie.id).add_entity(Movie).join(User, session['user_id'] == User.id).add_entity(User).paginate(page=page, per_page=10)
    return render_template("home/moviecol.html", page_data=page_data)


# 上映预告
@home.route("/animation/")
def animation():
    data = Preview.query.all()
    return render_template("home/animation.html", data=data)

# 电影搜索页面
@home.route("/search/<int:page>/", methods=['GET', 'POST'])
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    movie_count = Movie.query.filter(Movie.title.ilike('%' + key + '%')).count()
    page_data = Movie.query.filter(Movie.title.ilike('%' + key + '%')).order_by(Movie.addtime.desc()).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template("home/search.html", key=key, page_data=page_data, movie_count=movie_count)

# 电影播放页面
@home.route("/play/<int:id>/<int:page>/", methods=['GET', 'POST'])
def play(id=None, page=None):
    movie = Movie.query.join(Tag, and_(Movie.tag_id == Tag.id, Movie.id == int(id))).add_entity(Tag).first()
    
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie, Comment.movie_id == Movie.id).add_entity(Movie).join(User, Comment.user_id == User.id).add_entity(User).order_by(Comment.addtime.desc()).paginate(page=page, per_page=10)
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.Movie.id,
            user_id=session['user_id'],
            addtime=current_time
        )
        db.session.add(comment)
        db.session.commit()
        # db.session.close()
        movie.Movie.commentnum += 1
        db.session.add(movie.Movie)
        db.session.commit()
        flash(u"添加评论成功", "ok")
        return redirect(url_for('home.play', id=movie.Movie.id, page=1))
    print(movie.Movie.playnum)
    movie.Movie.playnum += 1
    print(movie.Movie.playnum)
    db.session.add(movie.Movie)
    db.session.commit()
    return render_template("home/play.html", movie=movie, form=form, page_data=page_data)



@home.route("/video/<int:id>/<int:page>/", methods=['GET', 'POST'])
def video(id=None, page=None):
    movie = Movie.query.join(Tag, and_(Movie.tag_id == Tag.id, Movie.id == int(id))).add_entity(Tag).first()
    
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie, Comment.movie_id == Movie.id).add_entity(Movie).join(User, Comment.user_id == User.id).add_entity(User).order_by(Comment.addtime.desc()).paginate(page=page, per_page=10)
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.Movie.id,
            user_id=session['user_id'],
            addtime=current_time
        )
        db.session.add(comment)
        db.session.commit()
        # db.session.close()
        movie.Movie.commentnum += 1
        db.session.add(movie.Movie)
        db.session.commit()
        flash(u"添加评论成功", "ok")
        return redirect(url_for('home.video', id=movie.Movie.id, page=1))
    print(movie.Movie.playnum)
    movie.Movie.playnum += 1
    print(movie.Movie.playnum)
    db.session.add(movie.Movie)
    db.session.commit()
    return render_template("home/video.html", movie=movie, form=form, page_data=page_data)





# @app.route('/video/<int:id>/<int:page>/', methods=["GET", "POST"])
# def video(id=None, page=None):
    movie = Movie.query.join(Tag, and_(Movie.tag_id == Tag.id, Movie.id == int(id))).add_entity(Tag).first()
    
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie, Comment.movie_id == Movie.id).add_entity(Movie).join(User, Comment.user_id == User.id).add_entity(User).order_by(Comment.addtime.desc()).paginate(page=page, per_page=10)
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.Movie.id,
            user_id=session['user_id'],
            addtime=current_time
        )
        db.session.add(comment)
        db.session.commit()
        # db.session.close()
        movie.Movie.commentnum += 1
        db.session.add(movie.Movie)
        db.session.commit()
        flash(u"添加评论成功", "ok")
        return redirect(url_for('home.video', id=movie.Movie.id, page=1))
    print(movie.Movie.playnum)
    movie.Movie.playnum += 1
    print(movie.Movie.playnum)
    db.session.add(movie.Movie)
    db.session.commit()
    return render_template("home/video.html", movie=movie, form=form, page_data=page_data)

@home.route("/tm/", methods=["GET", "POST"])
def tm():
    import json
    if request.method == "GET":
        #获取弹幕消息队列
        id = request.args.get('id')
        key = "movie" + str(id)
        if rd.llen(key):
            msgs = rd.lrange(key, 0, 2999)
            res = {
                "code": 1,
                "danmaku": [json.loads(v) for v in msgs]
            }
        else:
            res = {
                "code": 1,
                "danmaku": []
            }
        resp = json.dumps(res)
    if request.method == "POST":
        #添加弹幕
        data = json.loads(request.get_data())
        msg = {
            "__v": 0,
            "author": data["author"],
            "time": data["time"],
            "text": data["text"],
            "color": data["color"],
            "type": data['type'],
            "ip": request.remote_addr,
            "_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
            "player": [
                data["player"]
            ]
        }
        res = {
            "code": 1,
            "data": msg
        }
        resp = json.dumps(res)
        rd.lpush("movie" + str(data["player"]), json.dumps(msg))
    return Response(resp, mimetype='application/json')

