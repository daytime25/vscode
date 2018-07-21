# coding: utf-8
from flask import Flask,render_template,url_for,jsonify #生成Flask实例 
import json
from flask_sqlalchemy import SQLAlchemy
from createtable import waterwork1




#data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]
app = Flask(__name__)



@app.route('/weather', methods=['GET','POST'])
def my_echart(): #在浏览器上渲染my_templaces.html模板
    
    '''res = [(1, 2, 2.6),
             (2, 4.9, 5.9),
             (3, 7, 9),
             (4, 23.2, 26.4),
             (5, 25.6, 28.7),
             (6, 76.7, 70.7),
             (7, 135.6, 175.6),
             (8, 162.2, 182.2),
             (9, 32.6, 48.7),
             (10, 20, 18.8),
             (11, 6.4, 6),
             (12, 3.3, 2.3)
            ]
    data=jsonify(month = [x[0] for x in res],
    evaporation = [x[1] for x in res],
    precipitation = [x[2] for x in res])'''
    cc=waterwork1.query.all()

    return render_template('my_template.html',data=cc)

if __name__ == "__main__": #运行项目 
    app.run(debug = True) 