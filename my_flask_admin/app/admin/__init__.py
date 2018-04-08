#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from flask import Blueprint

admin = Blueprint("admin", __name__)
import app.admin.views