
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

@app.route('/api/v1/employees', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Name'], content['Sex'], content['Age'],
                 content['Height_in'], content['Weight_lbs'])
    sql_insert_query = """INSERT INTO employeeInfo (Name, Sex, Age, Height_in, Weight_lbs) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/employees/<int:emp_id>', methods=['PUT'])
def api_edit(emp_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Name'], content['Sex'], content['Age'],
                 content['Height_in'], content['Weight_lbs'],emp_id)
    sql_update_query = """UPDATE employeeInfo e SET e.Name = %s, e.Sex = %s,e.Age = %s, e.Height_in = %s, e.Weight_lbs = 
    %s WHERE e.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/employees/<int:emp_id>', methods=['DELETE'])
def api_delete(emp_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM employeeInfo WHERE id = %s """
    cursor.execute(sql_delete_query, emp_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
