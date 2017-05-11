from flask import render_template, request
from flask import Flask
from psql_interface import psql_connection


import json
import threading
import time
import sys 

app = Flask(__name__)
#app.config['PROPAGATE_EXCEPTIONS'] = True
#app.config['DEBUG'] = True
name = "measure_device_base"
user = "pmezydlo"
host = "localhost"
password = "pass"

base = psql_connection(name, user, host, password)

@app.route('/api/dev', methods=['POST', 'GET'])
def add_device():
    if request.method == 'POST':
        base.add_device_json(request.data)   
    return base.get_devices_list_json()

@app.route('/api/task', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        base.add_task_json(request.data)
        print request.data
    return base.get_tasks_list_json()

@app.route('/api/task/<task_id>', methods=['DELETE'])
def del_task(task_id):
    base.del_task_by_id(task_id)
    return base.get_tasks_list_json()

@app.route('/api/dev/<dev_id>', methods=['DELETE'])
def del_device(dev_id):
    base.del_device_by_id(dev_id)
    return base.get_devices_list_json()

@app.route('/api/sys/stop', methods=['POST'])
def sysStop():
    print "stop"
    return 'ok status'

@app.route('/api/sys/start', methods=['POST'])
def sysStart():
    print "start"
    return 'ok status'

@app.route("/api/logs", methods=['GET', 'DELETE'])
def get_logs():
    if request.method == 'DELETE':
        base.del_logs()
    return base.get_logs_json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route(/api/sys/dt)
def get_dt:
    dt = datetime.datetime.now()
    d = dt.strftime("%d.%m.%y")
    t = dt.strftime("%H:%M:%S")
return 'dt' 

@app.before_first_request
def active_core():
    base.push_log_msg('SERVER', 'LOG', "Server is up")

def main():
    app.run()

if __name__ == "__main__":
    main()

