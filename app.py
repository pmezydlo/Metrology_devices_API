from flask import render_template, request
from flask import Flask
from psql_interface import psql_connection
from maincore import *
import datetime
import json

app = Flask(__name__)
#app.config['PROPAGATE_EXCEPTIONS'] = True
#app.config['DEBUG'] = True
name = "measure_device_base"
user = "pmezydlo"
host = "localhost"
password = "pass"

core = maincore(name, user, password, host)
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

@app.route("/api/logs", methods=['GET', 'DELETE'])
def get_logs():
    if request.method == 'DELETE':
        base.del_logs()
    return base.get_logs_json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sys", methods=['GET'])
def get_dt():
    dt = datetime.datetime.now()
    d = dt.strftime("%d.%m.%y")
    t = dt.strftime("%H:%M:%S")
    ret = {u"date": d, u"time": t, u"core_run": core.run_signal}
    return json.dumps(ret)

@app.before_first_request
def active_core():
    base.push_log_msg('SERVER', 'LOG', "Server is up")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/api/sys/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    core.exit_signal = True
    core.join()
    base.psql_disconnect()
    return 'Server shutting down...'
 
@app.route('/api/sys/stop', methods=['POST'])
def sysStop():
    core.run_signal = False
    return 'ok'

@app.route('/api/sys/start', methods=['POST'])
def sysStart():
    core.run_signal = True
    return 'ok'

def main():
        core.start()
        app.run()    

if __name__ == "__main__":
    main()

