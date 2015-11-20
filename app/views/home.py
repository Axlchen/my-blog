#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015年11月15日

@author: axlchen
'''

import re
from flask import render_template,Blueprint,request,url_for,redirect,session,flash
from conf.development import PER_PAGE
from app import models
home = Blueprint('home', __name__)

@home.route('/')
def index():
    cat = models.Category()
    #文章分类
    cats = cat.getCatAndQuantity(front=1)
    #文章列表
    article = models.Article()
    articles = article.getArticle(noprivate=1)
    #文章数量
    total = article.getArticleNum(front=1)
    #时间归档
    timeset = article.timeAndQuantity(front=1)
    return render_template('home/index.html',title="Blog of Axlchen",\
                           categorys=cats,articles=articles,page=0,total=total,perpage=PER_PAGE,timeset=\
                           timeset)

@home.route('/articles/page/<int:page_id>')
def mainPage(page_id):
    cat = models.Category()
    #文章分类
    cats = cat.getCatAndQuantity(front=1)
    #文章列表
    article = models.Article()
    articles = article.getArticle(offset=(page_id-1)*PER_PAGE,noprivate=1)
    #文章数量
    total = article.getArticleNum(front=1)
    #时间归档
    timeset = article.timeAndQuantity(front=1)
    return render_template('home/index.html',title="文章列表|Blog of Axlchen",\
                           categorys=cats,articles=articles,page=page_id,total=total,perpage=PER_PAGE,\
                           timeset=timeset)
    
@home.route('/category/<int:cat_id>/page/<int:page_id>')
def getArticleByCat(cat_id,page_id):
    #文章分类
    cat = models.Category()
    cats = cat.getCatAndQuantity(front=1)
    #分类名称
    catname = cat.getCatName(cat_id)
    #该分类的文章数量
    article = models.Article()
    articles = article.getArticle(cat=cat_id,offset=(page_id-1)*PER_PAGE,noprivate=1)
    total = article.getCatOfArtNum(cat_id,front=1)
    #时间归档
    timeset = article.timeAndQuantity(front=1)
    return render_template('home/index.html',title=catname+"|Blog of Axlchen",\
                           categorys=cats,articles=articles,catid=cat_id,catpage=page_id,total=total,\
                           perpage=PER_PAGE,timeset=timeset)

@home.route('/articles/<int:time_id>/page/<int:page_id>')
def getArticleByTime(time_id,page_id):
    #文章分类
    cat = models.Category()
    cats = cat.getCatAndQuantity(front=1)
    #该时间分类的文章和总数
    article = models.Article()
    articles = article.getArticle(time_id=time_id,offset=(page_id-1)*PER_PAGE,noprivate=1)
    total = article.getTimeOfArtNum(time_id)
    #时间归档
    timeset = article.timeAndQuantity(front=1)
    #年月
    yandm = str(time_id)[0:4]+'年'+str(time_id)[-2:]+'月'
    return render_template('home/index.html',title=yandm+"|Blog of Axlchen",categorys=cats,articles=articles,\
                           timepage=page_id,timeid=time_id,total=total,perpage=PER_PAGE,timeset=timeset)

@home.route('/articles/<int:aid>')
def getarticlebyid(aid):
    #获取文章类别
    cat = models.Category()
    cats = cat.getCatAndQuantity(front=1)
    #获取文章
    article = models.Article()
    singleArticle = article.getById(aid)
    #获取文章评论
    comment = models.Comment()
    comments = comment.getByAid(aid, front=1)
    #时间归档
    timeset = article.timeAndQuantity(front=1)
    return render_template('home/article.html',title=singleArticle[0]+"|Blog of Axlchen",categorys=cats,\
                           article=singleArticle,timeset=timeset,aid=aid,comments=comments)

@home.route('/comment',methods=['POST'])
def comment():
    if request.method == 'GET':
        pass
    aid = request.form['artnum']
    nickname = request.form['nickname']
    email = request.form['email']
    content = request.form['content']
    comment = models.Comment()
    if not re.match('^\w+@[^0-9\.]\w+\.[a-zA-Z\.]{1,6}$', email):
        return '请填写正确的邮件地址'
    res = comment.addComment(aid, nickname, email, content)
    if not res:
        return comment.error
    else:
        return 'success'





