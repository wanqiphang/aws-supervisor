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

# Initialize the S3 client
s3 = boto3.client('s3', region_name=region)

# Function to read files from S3
def read_file_from_s3(file_key):
    try:
        response = s3.get_object(Bucket=bucket, Key=file_key)
        file_content = response['Body'].read()
        return file_content.decode('utf-8')  # Assuming it's text content
    except Exception as e:
        print(f"An error occurred while reading {file_key} from S3: {str(e)}")
        return None


# routes
@app.route("/Supervisor")
def indexSupervisor():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM StudentInfo')
    data = cursor.fetchall()
    cursor.close()
    
    # Read files from S3 (replace 'file_key' with the actual file key)
    file_key = 'your-file-key'
    file_content = read_file_from_s3(file_key)

    return render_template('index.html', StudentInfo = data, file_content=file_content)

@app.route("/Form")
def Form():
    cursor = db_conn.cursor()
    cursor.execute('SELECT student_name, student_id FROM StudentInfo')
    data = cursor.fetchall()
    cursor.close()
    
    # Read files from S3 (replace 'file_key' with the actual file key)
    file_key = 'your-file-key'
    file_content = read_file_from_s3(file_key)

    return render_template('Form.html', StudentInfo=data, file_content=file_content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)