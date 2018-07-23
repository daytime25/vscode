#coding: utf-8
import shelve
from flask import Flask, request, render_template, redirect, escape, Markup

DATA_FILE='guestbook.dat'

application = Flask(__name__)

def save_data(name,comment,create_at):
    """
    """
    database=shelve.open(DATA_FILE)
    if 'greeting_list' not in database:
        greeting_list=[]
    else:
        greeting_list=database['greeting_list']
    greeting_list.insert(0,{'name': name,'comment': comment,'create_at': create_at,})
    database['greeting_list']=greeting_list
    database.close()

def load_data():
    """ 返回已提交的数据
"""
# 通过 shelve 模块打开数据库文件
    database = shelve.open(DATA_FILE)
# 返回 greeting_list。如果没有数据则返回空表
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list

@application.route('/')
def index():
    greeting_list=load_data()
    return render_template('index.html',greeting_list=greeting_list)

if __name__ == '__main__':
    application.run(debug=True)