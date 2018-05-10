#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from flask.ext.redis import FlaskRedis
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/movie"
# 追踪对象的修改且发送信号  需要内存  可以禁用
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'wewe3.ewe$'
app.config["REDIS_URL"] = "redis://127.0.0.1:6379"
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/users/')
db = SQLAlchemy(app)
app.debug = False
rd = FlaskRedis(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")

# 定义错误页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
