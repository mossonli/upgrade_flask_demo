#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from . import admin


@admin.route("/")
def index():
    return "<h1 style='color:red'>this is admin<h1>"