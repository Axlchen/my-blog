#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015年11月15日

@author: axlchen
'''

import sae.const
DEBUG = True
MYSQL_HOST = sae.const.MYSQL_HOST    # 主库域名（可读写）
MYSQL_USER = sae.const.MYSQL_USER    # 用户名
MYSQL_PASS = sae.const.MYSQL_PASS    # 密码
MYSQL_DB   = sae.const.MYSQL_DB      # 数据库名
MYSQL_PORT = sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
PER_PAGE   = 5
