#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015年11月15日

@author: axlchen
'''

from flask import Flask

app = Flask(__name__,)
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('conf.development')
app.config.from_pyfile('config.py')
#注册蓝图
from .views.admin import admin
app.register_blueprint(admin)