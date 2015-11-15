#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015年11月15日

@author: axlchen
'''
from app.views import home
from app import app
#以下三行解决 UnicodeDecodeError: 'ascii' 错误
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    app.run()

