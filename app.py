from flask import render_template, request
from flask import Flask
import json
import threading
import time
import sys 
from psql_interface import psql_connection
from device_interface import dev_core

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = True

device_thread_list = []
name = "measure_device_base"
user = "pmezydlo"
host = "localhost"
password = "pass"
base = psql_connection(name, user, host, password)

@app.route('/api/dev', methods=['POST', 'GET'])
def add_device():
    if request.method == 'POST':
        base.add_device_json(request.data)   
        base.push_log_msg('add new device', 'log')
    return base.get_devices_list_json()

@app.route('/api/dev/<dev_id>', methods=['DELETE'])
def del_device(dev_id):
    base.del_device_by_id(dev_id)
    return base.get_devices_list_json()

@app.route("/api/dev/act/<dev_id>", methods=['POST'])
def act_device(dev_id):
    if request.method == 'POST':
        print "act device"
        print request.data
        
    return 200 

@app.route("/api/logs", methods=['GET', 'DELETE'])
def get_logs():
    if request.method == 'DELETE':
        base.del_logs()
    return base.get_logs_json()

@app.route("/")
def index():
    return render_template("index.html")

def main():
    pass

if __name__ == "__main__":
    app.run(threaded=True)
    main()


# how to run your own code in flask
# update angular script for each server running
# static angular js script
# flask and thread how it works
# add async request to server with angular

