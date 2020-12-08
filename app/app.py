
from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'employeeData'
mysql.init_app(app)




@app.route('/api/v1/employees', methods=['GET'])
def api_browse()-> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/employees/<int:emp_id>', methods=['GET'])
def api_retrieve(emp_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo WHERE id=%s', emp_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
