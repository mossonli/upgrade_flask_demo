#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from app import db
from datetime import datetime


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.Integer, index=True)
    uuid = db.Column(db.String(255), unique=True)
    # userlogs = db.relationship("userlog", backref="user")
    # comments = db.relationship("Comment", backref="user")
    # moviecols = db.relationship("movieCols", backref="user")

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

# 会员登录日志
class UserLog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.Integer, index=True)
    
    def __repr__(self):
        return "<userLog %r>" % self.id


# 标签 
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.Integer, index=True)
    # movies = db.relationship("Movie", backref="tag")

    def __repr__(self):
        return "<Tag %r>" % self.name


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.Integer)
    playnum = db.Column(db.Integer)
    commentnum = db.Column(db.Integer)    
    # tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    tag_id = db.Column(db.Integer)
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.Integer, index=True)
    # comments = db.relationship("Comment", backref="movie")  # 评论
    # moviecols = db.relationship("movieCol", backref="movie") # 收藏 
    
    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.Integer, index=True)

    def __repr__(self):
        return "<Preview %r>" % self.title


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    # movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    addtime = db.Column(db.Integer, index=True)

    def __repr__(self):
        return "<Comment %r>" % self.id


# class Comment(db.Model):
#     __tablename__ = "comment"
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text)
#     movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     addtime = db.Column(db.DateTime, index=True, default=datetime.now)

#     def __repr__(self):
#         return "<Comment %r>" % self.id


class MovieCol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    addtime = db.Column(db.Integer, index=True)

    def __repr__(self):
        return "<movieCol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.Integer)

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600)) # 角色权限列表
    addtime = db.Column(db.Integer, index=True)
    # admins = db.relationship("Admin", backref="role")

    def __repr__(self):
        return "<Role %r>" % self.name


#  管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.Integer)
    # role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role_id = db.Column(db.Integer)
    addtime = db.Column(db.Integer, index=True)
    # adminlogs = db.relationship("adminLog", backref="admin") # 管理员登录日志
    # oplogs = db.relationship("opLog", backref="admin") # 管理员操作日志

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class AdminLog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer)
    # admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    ip = db.Column(db.String(255))
    addtime = db.Column(db.Integer, index=True)

    def __repr__(self):
        return "<adminlog %r>" % self.id


class OpLog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer)
    # admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    ip = db.Column(db.String(255))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.Integer, index=True)

    def __repr__(self):
        return "<oplog %r>" % self.id


    