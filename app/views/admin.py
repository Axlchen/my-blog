#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015年11月15日

@author: axlchen
'''

from flask import render_template,Blueprint
from app import app

admin = Blueprint('admin', __name__)


@admin.route('/backyard')
def index():
    return render_template('admin/index.html')

@admin.route('/by/login')
def login():
    return render_template('admin/login.html') 
    
    
@admin.route('/by/admin')
def main():
    return render_template('admin/admin.html')

@admin.route('/by/write')
def write():
    return render_template('admin/write.html')

@admin.route('/by/modify')
def modify():
    return render_template('admin/modify.html')

@admin.route('/by/commentview')
def commentview():
    return render_template('admin/commentfix.html')

@admin.route('/by/decomment')
def decomment():
    return render_template('admin/commentfix2.html')



