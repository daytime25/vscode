#-*- coding:utf-8 -*-
from flask import Flask, render_template,request,Response,session,redirect,url_for,flash,jsonify
import json
import mysql.connector
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from mysql2 import sqljs 

app = Flask(__name__)
bootstrap = Bootstrap(app)

config={'host':'172.16.14.222',#默认127.0.0.1
        'user':'root',
        'password':'123456',
        'port':3306 ,#默认即为3306
        'database':'shunyizilaishui',
        'charset':'utf8'#默认即为utf8
        }
cnx = mysql.connector.connect(**config)


def Response_headers(content):  
    resp = Response(content)  
    resp.headers['Access-Control-Allow-Origin'] = '*'  
    resp.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE' 
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return resp



@app.route('/')
def index():
    return render_template('index.html')

@app.route("/weather", methods=["GET","POST"])
def weather():
    if request.method == "GET":
        res = query_db("SELECT * FROM weather WHERE id <= 6") #不妨设定：第一次只返回6个数据
    elif request.method == "POST":
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        js_data=sqljs(json_data['shuichang'],json_data['logdate1'],json_data['logdate2'])
        #print(json_data['shuichang'],js_data)
        #return json.dumps(js_data)
        resp = Response_headers(js_data)
        return resp

@app.route('/add')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/page', methods=['GET', 'POST'])
def page():
    
    return render_template('page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template('login.html')

@app.route('/page1')
def take_login():
    return render_template('page1.html')

@app.route('/caa', methods=["GET","POST"])
def caa():
    if request.method == "POST":
        data = request.get_data()
        print(data.decode("utf-8"))
        data = json.loads(data.decode("utf-8"))
    return "46575"
    
    

def selcity(city):
    sql="SELECT 部门 FROM `user` WHERE `名字`='"+city+"'"
    cursor = cnx.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    results=result[0]
    return results



@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

@app.route('/echarts',methods=['GET', 'POST'])  
def echarts():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    js_data=sqljs(json_data['shuichang'],json_data['logdate1'],json_data['logdate2'])
    #print(json_data['shuichang'],js_data)
    #return json.dumps(js_data)
    resp = Response_headers(js_data)
    return resp
    


@app.route('/json')  
def ja():
    datas = {
		"data":[
			{"name":"allpe","num":100},
			{"name":"peach","num":123},
			{"name":"Pear","num":234},
			{"name":"avocado","num":20},
			{"name":"cantaloupe","num":1},
			{"name":"Banana","num":77},
			{"name":"Grape","num":43},
			{"name":"apricot","num":0}
		]
	}
    content = json.dumps(datas)
    resp = Response_headers(content)
    return resp


 
@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp
 




if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
    