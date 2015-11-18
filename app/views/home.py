#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015年11月15日

@author: axlchen
'''

from flask import render_template,Blueprint,request,url_for,redirect,session,flash
from conf.development import PER_PAGE
from app import models
home = Blueprint('home', __name__)


@home.route('/')
def index():
    cat = models.Category()
    #文章分类
    cats = cat.getCatAndQuantity()
    #文章列表
    article = models.Article()
    articles = article.getArticle()
    #文章数量
    total = article.getArticleNum()
    return render_template('home/index.html',title="Blog of Axlchen",\
                           categorys=cats,articles=articles,page=0,total=total,perpage=PER_PAGE)

@home.route('/articles/page/<int:page_id>')
def mainPage(page_id):
    cat = models.Category()
    #文章分类
    cats = cat.getCatAndQuantity()
    #文章列表
    article = models.Article()
    articles = article.getArticle(offset=(page_id-1)*PER_PAGE)
    #文章数量
    total = article.getArticleNum()
    return render_template('home/index.html',title="文章列表|Blog of Axlchen",\
                           categorys=cats,articles=articles,page=page_id,total=total,perpage=PER_PAGE)
    
@home.route('/category/<int:cat_id>/page/<int:page_id>')
def getArticleByCat(cat_id,page_id):
    #文章分类
    cat = models.Category()
    cats = cat.getCatAndQuantity()
    #分类名称
    catname = cat.getCatName(cat_id)
    #该分类的文章数量
    article = models.Article()
    articles = article.getArticle(cat=cat_id,offset=(page_id-1)*PER_PAGE)
    total = article.getCatOfArtNum(cat_id)
    return render_template('home/index.html',title=catname+"|Blog of Axlchen",\
                           categorys=cats,articles=articles,catid=cat_id,catpage=page_id,total=total,perpage=PER_PAGE)

@home.route('/articles/<int:aid>')
def getarticlebyid(aid):
    #获取文章类别
    cat = models.Category()
    cats = cat.getCatAndQuantity()
    #获取文章
    article = models.Article()
    singleArticle = article.getById(aid)
    return render_template('home/article.html',title=singleArticle[0]+"|Blog of Axlchen",categorys=cats,article=singleArticle)









