#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015年11月15日

@author: axlchen
'''
from flask import g
from app import app
import MySQLdb,hashlib,time
from conf.production import MYSQL_HOST,MYSQL_USER,MYSQL_PASS,MYSQL_DB,MYSQL_PORT,PER_PAGE

@app.before_request
def before_request():
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB, port=int(MYSQL_PORT))
     
@app.teardown_request
def teardown_request(exception):
    g.db.close()

class Model:
    def __init__(self):
        self.cursor=g.db.cursor()
        self.error=None
    
    def __del__(self):
        self.cursor.close()
        
class User(Model):
    __table = 'user'
                
    def auth(self,username,password):
        self.cursor.execute("""select * from user where username=%s""",(username,))
        data = self.cursor.fetchone()
        if data is not None:
            m = hashlib.md5()
            m.update(password)
            if m.hexdigest() == data[2]:
                return True
            else:
                self.error = '密码错误'
                return False
        else:
            self.error = '用户名错误'
            return False
    
class Category(Model):
    __table = 'category'
    __atable = 'article'
    
    def getAll(self):
        self.cursor.execute('select id,cat_name from %s' % self.__table)
        return self.cursor.fetchall()
    
    def getCatName(self,cat_id):
        self.cursor.execute('select cat_name from %s where id=%s' % (self.__table,cat_id))
        res = self.cursor.fetchone()
        return res[0]
        
    def getCatAndQuantity(self):
        self.cursor.execute('select tmp.cid,tmp.cat_name,count(tmp.category) from (select %s.id as cid,cat_name,category \
                            from %s left join %s on %s.id=%s.category) \
                            as tmp group by tmp.cat_name' % (self.__table,self.__table,self.__atable,\
                                                             self.__table,self.__atable))
        return self.cursor.fetchall()
            
    def add(self,cat_name):
        self.cursor.execute('select * from %s where cat_name="%s"' % (self.__table,cat_name))
        if self.cursor.fetchone() is not None:
            self.error = '分类已存在'
            return False
        self.cursor.execute('insert into %s(cat_name) values("%s")' % (self.__table,cat_name))
        lid = g.db.insert_id()
        if not lid:
            self.error = '增加失败'
            g.db.rollback()
            return False
        else:
            g.db.commit()
            return True
            
class Article(Model):
    __table = 'article'
    __ctable = 'category'
#     __output = []
    
    def formatTime(self,inputvar,index):
        inputvar[index] = str(time.localtime(inputvar[index])[0])+'-'+str(time.localtime(inputvar[index])[1])+'-'+\
        str(time.localtime(inputvar[index])[2])+' '+str(time.localtime(inputvar[index])[3])+':'+\
        str(time.localtime(inputvar[index])[4])
        return inputvar
    
    def tupleToList(self,inputvar):
        output=[]
        for item in inputvar:
            if not isinstance(item,tuple):
                output.append(item)
            else:
                self.tupleToList(item)
        return output
    
    def add(self,title,content,category,private,desc):
        add_time = int(time.time())
        update_time = int(time.time())
        self.cursor.execute("insert into %s(title,description,content,category,is_private,add_time,update_time) values('%s','%s','%s',%s,%s,%s,%s)" \
                            % (self.__table,title,desc,content,category,private,add_time,update_time))
        lid = g.db.insert_id()
        if not lid:
            self.error = '发表失败'
            g.db.rollback()
            return False
        else:
            g.db.commit()
            return True
    def modify(self,title,description,content,category,private,aid):
        update_time = int(time.time())
        self.cursor.execute("update %s set title='%s',description='%s',content='%s',category=%s,is_private=%s,update_time=%s where id=%s"\
                            % (self.__table,title,description,content,category,private,update_time,aid))
        arows = g.db.affected_rows()
        if not arows:
            self.error = '修改失败'
            g.db.rollback()
            return False
        else:
            g.db.commit()
            return True
        
    def getArticleNum(self):
        self.cursor.execute('select count(*) from %s' % self.__table)
        res = self.cursor.fetchone()
        return res[0]
    
    def getCatOfArtNum(self,cat_id):
        self.cursor.execute('select count(*) from %s where category=%s' % (self.__table,cat_id))
        res = self.cursor.fetchone()
        return res[0]
    
    def getArticle(self,cat=0,offset=0,num=PER_PAGE):
        if not cat:     #没有指定分类
            self.cursor.execute('select title,description,cat_name,add_time,%s.id from %s left join %s on \
                                %s.category=%s.id order by %s.add_time desc limit %s,%s' \
                                % (self.__table,self.__table,self.__ctable,self.__table,self.__ctable,\
                                   self.__table,offset,num))
            res = self.cursor.fetchall()
        else:           #指定分类
            self.cursor.execute('select title,description,cat_name,add_time,%s.id from %s left join %s on \
                                %s.category=%s.id where %s.category=%s order by %s.add_time desc limit %s,%s' \
                                % (self.__table,self.__table,self.__ctable,self.__table,self.__ctable,\
                                   self.__table,cat,self.__table,offset,num))
            res = self.cursor.fetchall()
        reslist = [] 
        for item in res:
            result = self.tupleToList(item)
            result = self.formatTime(result, 3)
            reslist.append(result)
        return reslist
    
    def getById(self,cid):
        self.cursor.execute('select title,description,content,category,is_private,update_time from %s where id=%s' % (self.__table,cid))
        res = self.cursor.fetchone()
        res = self.tupleToList(res)
        return self.formatTime(res, 5)
        
            

class Comment(Model):
    pass
    
        
        
        
        
        
        
        
        
        