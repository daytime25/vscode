# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json,datetime,time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost:3306/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class waterwork1(db.Model):
    """定义数据模型"""
    __tablename__ = 'waterwork1'
    riqi = db.Column(db.Date, primary_key=True)
    NO = db.Column(db.Integer, primary_key=True)
    chanshuiliang = db.Column(db.Integer)
    haodianliang = db.Column(db.Integer)
 
    def __init__(self,riqi,NO,chanshuiliang,haodianliang):
        self.riqi = riqi
        self.NO = NO
        self.chanshuiliang=chanshuiliang
        self.haodianliang=haodianliang
 
    

    '''def to_json(self):
        
        json_waterwork={
            'riqi':self.riqi.strftime('%Y-%m-%d'),
            'NO':self.NO,
            'chanshuiliang':self.chanshuiliang,
            'haodianliang':self.haodianliang
        }
        return json_waterwork'''

    def datetime_toString(dt):
        return dt.strftime("%Y-%m-%d")

    def __repr__(self):
        riri=self.riqi.strftime("%Y-%m-%d")
        #riri=json.dumps(riri)
        json_waterwork={
            'riqi':riri,
            'NO':self.NO,
            'chanshuiliang':self.chanshuiliang,
            'haodianliang':self.haodianliang
        }
        return '%r' % json_waterwork


class CJsonEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, datetime.date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj)  

if __name__ == "__main__": #运行项目 
    #db.create_all()
    '''c1=waterwork1('2018-03-02','1','84858','8848')
    c2=waterwork1('2018-03-02','2','84858','8848')
    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()'''
    
    cc=waterwork1.query.all()
    
   
    for c in cc:
        c.riqi=c.riqi.strftime('%Y-%m-%d')
        print (c.riqi,c.NO,c.chanshuiliang,c.haodianliang)
        data_riqi=json.dumps(c.riqi,cls=CJsonEncoder)
        print (c)
    print (cc)
    #执行sql的查询

    '''sql='SELECT * FROM test.waterwork1;'
    items=list()
# 执行sql ，返回值都是list()，要取值遍历，每一个直接通过'.字段名'的方式取指定的字段
    items=db.session.execute(sql)

    riqi=[it[0] for it in items]
    NO=[it[1] for it in items]
    chanshuiliang=[it[2] for it in items]
    haodianliang=[it[3] for it in items]
    print (riqi,NO,chanshuiliang,haodianliang)'''
    
