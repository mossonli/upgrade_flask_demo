#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'mosson'
from flask import Blueprint

home = Blueprint("home", __name__)
import app.home.views