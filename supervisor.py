from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)
app.secret_key = "Supervisor"

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)

output = {}
table = 'StudentInfo'


# routes
@app.route("/Supervisor")
def indexSupervisor():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM StudentInfo')
    data = cursor.fetchall()
    cursor.close()

    return render_template('index.html', StudentInfo = data)

@app.route("/Form")
def Form():
    cursor = db_conn.cursor()
    cursor.execute('SELECT student_name, student_id FROM StudentInfo')
    data = cursor.fetchall()
    cursor.close()

    return render_template('Form.html', StudentInfo=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)