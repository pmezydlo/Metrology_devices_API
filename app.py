#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''

'''

__author__ = "Patryk Mezydlo"
__copyright__ = "Copyright 2018, Metrology Device API"
__credits__ = ["Patryk Mezydlo"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Patryk Mezydlo"
__email__ = "mezydlo.p@gmail.com"
__status__ = "Development"

from flask import render_template, request, send_from_directory, Response
from flask import Flask
from datetime import datetime
from base_interface import *
from maincore import *
from system_interface import system_interface
from common_const import common_const 
import json
import os

app = Flask(__name__)
core = maincore()
system = system_interface()
const = common_const()

@app.route('/api/dev', methods=['POST', 'GET'])
def add_device():
    if request.method == 'POST':
        try:
            dev = json.loads(request.data.decode('utf-8'))
        except ValueError as e:
            Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Decoding JSON has failes by: {}".format(e))
        else:
            if 'name' in dev and 'lan_address' in dev:
                new_dev = Device.create(name=dev["name"], lan_address=dev["lan_address"], status=DevStatusType.Offline.value)
                Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="{} device was added".format(new_dev.name))
            else:
                Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Device was not added, required fields not exist")

    ret_list = []
    for dev in Device.select():
        ret_list.append (dev.get_json())
    try:
        return json.dumps(ret_list)
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/api/dev/<dev_id>', methods=['DELETE'])
def del_device(dev_id):
    query = Device.select().where(Device.id == dev_id)
    if query:
        dev = query.get()
        Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="{} device was deleted.".format(dev.name))
        dev.delete_instance()
    else:
        Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="Device not exists.".format(dev.name))

    ret_list = []
    for dev in Device.select():
        ret_list.append (dev.get_json())
    try:
        return json.dumps(ret_list)
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/api/detectDev', methods=['POST'])
def autodetect_device():
    # wake detecting device event
    core.detect = True
    return 'Detecting LXI devices was runned'

@app.route('/api/checkDev/<devID>', methods=['POST'])
def check_device_connection(devID): # TODO: add suport for checking connection 
    #print "check conn"
    return 'Check connecting to device was runned'

@app.route('/api/results', methods=['GET'])
def get_results():
    ret_list = []
    for res in TaskResp.select().join(Task):
        ret_list.append (res.get_json())
    try:
        return json.dumps(ret_list)
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/api/results/<resID>', methods=['DELETE'])
def del_result(resID):
    query = TaskResp.select().where(TaskResp.id == resID)
    if query:
        res = query.get()
        Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="{} task results from {} was deleted".format(res.task.name, res.datetime_execute))
        res.delete_instance()
    ret_list = []
    for res in TaskResp.select().join(Task):
        ret_list.append (res.get_json())
    try:
        return json.dumps(ret_list)
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/api/cmds', methods=['GET'])
def get_cmds():
    cmds = []
    for filename in os.listdir(system.get_path()+const.CMDS_PATH()):
        try:
            file = open(system.get_path()+const.CMDS_PATH()+filename)
        except IOError as e:
            Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Open {} has failed: {}".format(filename, e))
        else:
            with file:
                try:
                    cmds.append(json.load(file))
                except ValueError as e:
                    Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Decoding JSON has failed by: {}".format(e))
    try:
        return json.dumps(cmds)
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/api/file', methods=['GET'])
def get_file():
    try:
        return json.dumps(system.get_file_info())
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/api/file/<name>', methods=['DELETE'])
def del_file(name):
    try:
        system.remove_file(name)
    except OSError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="File {} cannot be removed by: {}".format(name, e))
    try:
        return json.dumps(system.get_file_info())
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/files/<path:path>')
def send_file(path):
    return send_from_directory('files', path)

@app.route("/api/logs", methods=['GET', 'DELETE'])
def get_logs():
    if request.method == 'DELETE':
        for log in Log.select():
            log.delete_instance()
    ret = []
    for log in Log.select():
        ret.append(log.get_json())
    try:
        return json.dumps(ret) 
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route("/api/sys/info", methods=['GET'])
def get_sys_info():
    try:
        return json.dumps(system.get_system_information())
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route("/api/ver", methods=['GET'])
def get_ver():
    query = ServerVer.select()
    if query:
        ver = query.get()
        try:
            return json.dumps(ver.get_json())
        except TypeError as e:
            Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
            return 'Error, during serialized data', 500
    else:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during getting data', 500


@app.route('/api/task', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        try:
            task = json.loads(request.data.decode('utf-8'))
        except ValueError as e:
            Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Decoding JSON has failes by: {}".format(e))
        else:
            if 'name' in task and 'dev' in task and 'msg' in task:
                query = Device.select().where(Device.id == task["dev"])
                if query:
                    dev = query.get()
                    new_task = Task(name = task["name"],
                                    dev  = dev, 
                                    msg  = task["msg"])

                    if 'datetime_begin' in task:
                        new_task.datetime_begin = datetime.strptime(task["datetime_begin"], '%d/%m/%Y %H:%M:%S')
                        new_task.datetime_next = new_task.datetime_begin

                    if 'now' in task:
                        if task['now']:
                            new_task.datetime_begin = datetime.now()
                            new_task.datetime_next = new_task.datetime_begin

                    if 'datetime_end' in task:
                        new_task.datetime_end = datetime.strptime(task["datetime_end"], '%d/%m/%Y %H:%M:%S')

                    if 'series' in task:
                        new_task.series = task['series']
                        if 'cron_str' in task: 
                            new_task.cron_str = task['cron_str']

                    new_task.save()
                    Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="{} task was added".format(new_task.name))
                else:
                     Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Task was not added, desired device is not exist")
            else:
                Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Task was not added, required fields not exist")

    ret = []
    for task in Task.select():
        ret.append(task.get_json())
    try:
        return json.dumps(ret)
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/api/task/<task_id>', methods=['DELETE'])
def del_task(task_id):
    query = Task.select().where(Task.id == task_id)
    if query:
        task = query.get()
        Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="{} task was deleted".format(task.name))
        task.delete_instance()
    else:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Task id:{} does not exist".format(task_id))
    
    ret = []
    for task in Task.select():
        ret.append(task.get_json())
    try:
        return json.dumps(ret)
    except TypeError as e:
        Log.create(source=LogSourceType.Server.value, types=LogType.Error.value, msg="Unable to serialize the object:{}".format(e))
        return 'Error, during serialized data', 500

@app.route('/api/stopTask/<taskID>', methods=['POST'])
def stop_task(taskID):
    #print "stop task" # TODO: add support for stoping path
    return 'Task was stoped'

@app.route('/api/executeTask/<taskID>', methods=['POST'])
def executeTask(taskID): # TODO: add support for executing task manualy
    #print "execute now"
    return 'Task was runned manualy'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/sys/shutdown', methods=['POST'])
def shutdown():
    core.exit_signal = True
    core.join()
    Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="Server is down")
    base.close()
    return 'Server shutting down...'

@app.after_request
def inc_server_ver(response):
    if request.method != 'GET':
        query = ServerVer.select()
        if query:
            query.get().inc_runtime()
    return response

def main():
    base.connect()
    base.create_tables([Device, Task, Log, ServerVer, TaskResp])
    Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="Server is up")

    query = ServerVer.select()
    if not query:
        ServerVer.create(major=1, minor=0, runtime=0)
    core.start()
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

if __name__ == "__main__":
    main()
