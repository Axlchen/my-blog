#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015年11月15日

@author: axlchen
'''
from flask import render_template,Blueprint,request,url_for,redirect,session,flash
from conf.development import PER_PAGE
from app import models
admin = Blueprint('admin', __name__)


@admin.route('/backyard')
def index():
    return render_template('admin/index.html',title='Blog of Axlchen')

@admin.route('/by/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = models.User()
        if user.auth(username, password):
            session['auth_login'] = True
            return redirect(url_for('admin.main'))
        else:
            return render_template('admin/login.html',error=user.error,title='登陆|Blog of Axlchen')
    return render_template('admin/login.html',title='登陆|Blog of Axlchen')

@admin.route('/by/logout')
def logout():
    session['auth_login'] = False
    return redirect(url_for('admin.login'))
    
@admin.route('/by/admin',methods=['GET','POST'])
def main():
    cat = models.Category()
    if not session['auth_login']:
        flash('请先登陆')
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        res = cat.add(cat_name)
        if not res:
            return cat.error
        else:
            return '增加成功'
    #文章分类
    cats = cat.getCatAndQuantity()
    #文章列表
    article = models.Article()
    articles = article.getArticle()
    #文章数量
    total = article.getArticleNum()
    return render_template('admin/admin.html',title="Blog of Axlchen",\
                           categorys=cats,articles=articles,page=0,total=total,perpage=PER_PAGE)

@admin.route('/by/admin/page/<int:page_id>',methods=['GET','POST'])
def mainPage(page_id):
    cat = models.Category()
    if not session['auth_login']:
        flash('请先登陆')
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        res = cat.add(cat_name)
        if not res:
            return cat.error
        else:
            return '增加成功'
    #文章分类
    cats = cat.getCatAndQuantity()
    #文章列表
    article = models.Article()
    articles = article.getArticle(offset=(page_id-1)*PER_PAGE)
    #文章数量
    total = article.getArticleNum()
    return render_template('admin/admin.html',title="文章列表|Blog of Axlchen",\
                           categorys=cats,articles=articles,page=page_id,total=total,perpage=PER_PAGE)

@admin.route('/by/cat/<int:cat_id>/page/<int:page_id>',methods=['GET','POST'])
def getArticleByCat(cat_id,page_id):
    if not session['auth_login']:
        flash('请先登陆')
        return redirect(url_for('admin.login'))
    cat = models.Category()
    article = models.Article()
    if not session['auth_login']:
        flash('请先登陆')
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        cat_name = request.form['cat_name']
        res = cat.add(cat_name)
        if not res:
            return cat.error
        else:
            return '增加成功'
    #文章分类
    cats = cat.getCatAndQuantity()
    #分类名称
    catname = cat.getCatName(cat_id)
    #该分类的文章数量
    total = article.getCatOfArtNum(cat_id)
    articles = article.getArticle(cat=cat_id,offset=(page_id-1)*PER_PAGE)
    return render_template('admin/admin.html',title=catname+"|Blog of Axlchen",\
                           categorys=cats,articles=articles,catid=cat_id,catpage=page_id,total=total,perpage=PER_PAGE)

@admin.route('/by/write',methods=['GET','POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        private = request.form['auth']
        desc = request.form['shortdesc']
        article = models.Article()
        res = article.add(title, content, category, private,desc)
        if not res:
            return article.error
        else:
            return '发表成功'
    if not session['auth_login']:
        flash('请先登陆')
        return redirect(url_for('admin.login'))
    cat = models.Category()  
    cats = cat.getAll()
    return render_template('admin/write.html',title="撰写新文章|Blog of Axlchen",categorys=cats)

@admin.route('/by/modify/<int:art_id>',methods=['GET','POST'])
def modify(art_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['shortdesc']
        content = request.form['content']
        category = request.form['category']
        private = request.form['auth']
        article = models.Article()
        res = article.modify(title, description,content, category, private,art_id)
        if not res:
            return article.error
        else:
            return '修改成功'
    if not session['auth_login']:
        flash('请先登陆')
        return redirect(url_for('admin.login'))
    #获取文章类别
    cat = models.Category()
    cats = cat.getCatAndQuantity()
    #获取文章
    article = models.Article()
    singleArticle = article.getById(art_id)
    return render_template('admin/modify.html',title="修改文章|Blog of Axlchen",categorys=cats,\
                           aid=art_id,article=singleArticle)
    
@admin.route('/by/commentview')
def commentview():
    return render_template('admin/commentfix.html')

@admin.route('/by/decomment')
def decomment():
    return render_template('admin/commentfix2.html')




