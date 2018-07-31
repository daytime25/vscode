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

#同比
#SELECT t3.*,t4.* FROM (select t1.序号 AS xuhao,SUM(t1.`产水量`) AS chanshui from 一水厂 t1 where t1.日期 >= '2017-02-23' and t1.日期 <= '2018-02-23' and t1.序号 in('1','2','3','4','5','6','7') group by t1.序号 order by t1.序号) t3
#LEFT JOIN (SELECT t2.序号 AS qunianxuhao,SUM(t2.`产水量`) AS qunianchanshui from 一水厂 t2 where t2.日期 >= '2016-02-23' and t2.日期 <= '2017-02-23' and t2.序号 in('1','2','3','4','5','6','7') group by t2.序号 order by t2.序号) t4 ON t3.xuhao=t4.qunianxuhao;
#SELECT DATE_SUB('2017-02-23',INTERVAL 1 YEAR);在某个时间点减去某个时间

def sqljs(shuichang,logdate1,logdate2):
    if shuichang=="一水厂":
        select_sql=("SELECT 日期,SUM(一水厂.产水量) FROM shunyizilaishui.一水厂 WHERE 日期>='"+logdate1+"' AND 日期<='"+logdate2+"' AND 一水厂.序号 BETWEEN 1 AND 7 GROUP BY 一水厂.日期")
    elif shuichang=="二水厂":
         select_sql= ("SELECT 日期,SUM(二水厂.产水量) FROM shunyizilaishui.二水厂 WHERE 日期>='"+logdate1+"' AND 日期<='"+logdate2+"' AND 二水厂.序号 BETWEEN 1 AND 4 GROUP BY 二水厂.日期")
    elif shuichang=="同比":
         select_sql= ("SELECT t3.*,t4.* FROM (select t1.`日期` AS riqi,SUM(t1.`产水量`) AS chanshui from 一水厂 t1 where t1.日期 >= '"+logdate1+"' and t1.日期 <= '"+logdate2+"' and t1.序号 in('1','2','3','4','5','6','7') group by t1.`日期`) t3 \
         LEFT JOIN (SELECT t2.`日期` AS qunianriqi,SUM(t2.`产水量`) AS qunianchanshui from 一水厂 t2 where t2.日期 >= DATE_SUB('"+logdate1+"',INTERVAL 1 YEAR) and t2.日期 <= DATE_SUB('"+logdate2+"',INTERVAL 1 YEAR) and t2.序号 in('1','2','3','4','5','6','7') group by t2.`日期`) t4 \
         ON DATE_FORMAT(t3.riqi,'%m%d')=DATE_FORMAT(t4.qunianriqi,'%m%d');")
    
    
    try:
        cursor.execute(select_sql)# 执行SQL语句
        u=cursor.fetchall()# 获取所有记录列表
        # 转换成JSON数据格式
        jsonData = {}
        xdays = []
        yvalues = []
        xdays2 = []
        yvalues2 = []
        for data in u:
            # xdays.append(str(data[0]))
            xdays.append(data[0])
            yvalues.append(data[1])
            xdays2.append(data[2])
            yvalues2.append(data[3])
        print(xdays)
        print(yvalues)

        jsonData['xdays']=xdays
        jsonData['yvalues'] = yvalues
        jsonData['xdays2']=xdays2
        jsonData['yvalues2'] = yvalues2
        print(jsonData)
        
    except mysql.connector.Error as err:
        print("query table 'mytable' failed.")
        print("Error: {}".format(err.msg))
    else:
        #使用json.dumps将数据转换为json格式，json.dumps方法默认会输出成这种格式"\u5377\u76ae\u6298\u6263"，加ensure_ascii=False，则能够防止中文乱码。
        #JSON采用完全独立于语言的文本格式，事实上大部分现代计算机语言都以某种形式支持它们。这使得一种数据格式在同样基于这些结构的编程语言之间交换成为可能。
        #json.dumps()是将原始数据转为json（其中单引号会变为双引号），而json.loads()是将json转为原始数据。
        #字典是另一种可变容器模型，且可存储任意类型对象。字典的每个键值(key=>value)对用冒号(:)分割，每个对之间用逗号(,)分割，整个字典包括在花括号({})中 ,格式如下所示： 
        # json.dumps()用于将dict类型的数据转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
        j = json.dumps(jsonData)
        return (j)

if __name__ == "__main__":
    sqljs("同比","2018-01-12","2018-02-12")