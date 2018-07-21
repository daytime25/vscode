#-*- coding:utf-8 -*-

import mysql.connector
from flask import Flask, render_template,request,Response,session,redirect,url_for,flash
import json


config={'host':'172.16.14.222',#默认127.0.0.1
        'user':'root',
        'password':'123456',
        'port':3306 ,#默认即为3306
        'database':'shunyizilaishui',
        'charset':'utf8'#默认即为utf8
        }
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

    
select_sql = ("select 水源井号,日产水量,耗电量 from 第一水源地 where 日期 = '2016-01-23';")

def sql():
    try:
        cursor.execute(select_sql)# 执行SQL语句
        aa=cursor.fetchall()# 获取所有记录列表
        #data =cursor.fetchall()
        fields = cursor.description#获取列名
        list=[]
        col_list=[]
        for i in fields:
            col_list.append(i[0])
            #print (col_list)
        #print (col_list)
        for row in aa:
            result={}
            result['jinghao']=row[0]
            result['chanshuiliang']=str(row[1])
            result['haodianliang']=str(row[2])
            list.append(result)
        

        
       
            
    except mysql.connector.Error as err:
        print("query table 'mytable' failed.")
        print("Error: {}".format(err.msg))
    else:
        #使用json.dumps将数据转换为json格式，json.dumps方法默认会输出成这种格式"\u5377\u76ae\u6298\u6263"，加ensure_ascii=False，则能够防止中文乱码。
        #JSON采用完全独立于语言的文本格式，事实上大部分现代计算机语言都以某种形式支持它们。这使得一种数据格式在同样基于这些结构的编程语言之间交换成为可能。
        #json.dumps()是将原始数据转为json（其中单引号会变为双引号），而json.loads()是将json转为原始数据。
        #字典是另一种可变容器模型，且可存储任意类型对象。字典的每个键值(key=>value)对用冒号(:)分割，每个对之间用逗号(,)分割，整个字典包括在花括号({})中 ,格式如下所示： 
        data = json.dumps(list,ensure_ascii=False)
        #去除首尾的中括号
        return data

    #return data
    # js[3]["jinghao"],第三行的jinghao值
       
    




if __name__ == "__main__":
    print(sql())
    