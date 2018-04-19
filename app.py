from flask import render_template, request
from flask import Flask
from playhouse.shortcuts import model_to_dict, dict_to_model

from base_interface import *
#from maincore import *
from system_interface import system_interface
import datetime
import json

app = Flask(__name__)
#core = maincore(name, user, password, host)
system = system_interface()

@app.route('/api/dev', methods=['POST', 'GET'])
def add_device():
    if request.method == 'POST':
        dev = json.loads(request.data)
        new_dev = Device.create(name=dev["name"],
                        types=dev["types"], 
                        lan_address=dev["lan_address"],
                        lan_port=dev["lan_port"],
                        ps_channel=dev["ps_channel"])
        log = Log.create(source=LogSourceType.SERVER.value, types=LogType.LOG.value, msg="{} device was added".format(new_dev.name))
    ret = []
    for dev in Device.select():
        ret.append (dev.get_json())
    return json.dumps(ret) 

@app.route('/api/dev/<dev_id>', methods=['DELETE'])
def del_device(dev_id):
    dev = Device.select().where(Device.id == dev_id).get()
    log = Log.create(source=LogSourceType.SERVER.value, types=LogType.LOG.value, msg="{} device was deleted".format(dev.name))
    dev.delete_instance()
    ret = []
    for dev in Device.select():
        ret.append (dev.get_json())
    return json.dumps(ret)

@app.route("/api/logs", methods=['GET', 'DELETE'])
def get_logs():
    if request.method == 'DELETE':
        query = Log.delete()
        query.execute()
    ret = []
    for log in Log.select():
        ret.append (log.get_json())
    return json.dumps(ret) 

@app.route("/api/ver", methods=['GET'])
def get_ver():
    ver = ServerVer.select().get()
    return json.dumps(ver.get_json())

@app.route('/api/task', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        task = json.loads(request.data)
        inst_dev = Device.select().where(Device.id == task["dev"]).get()
        new_task = Task.create(name=task["name"], 
                        time=task["time"],
                        date=task["date"],
                        status=TaskStatusType.PENDING.value,
                        msg=task["msg"],
                        dev=inst_dev)
        log = Log(source=LogSourceType.SERVER.value, types=LogType.LOG.value, msg="{} task was added".format(new_task.name))
        log.save()
    ret = []
    for task in Task.select():
        ret.append(task.get_json())
    return json.dumps(ret) 

@app.route('/api/task/<task_id>', methods=['DELETE'])
def del_task(task_id):
    task = Task.select().where(Task.id == task_id).get()
    log = Log.create(source=LogSourceType.SERVER.value, types=LogType.LOG.value, msg="{} task was deleted".format(task.name))
    task.delete_instance()
    ret = []
    for task in Task.select():
        ret.append(task.get_json())
    return json.dumps(ret) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sys/info", methods=['GET'])
def get_sys_info(): 
    return system.get_system_information()

@app.after_request
def after_request(response):
    if request.method != 'GET':
        ver = ServerVer.select().get()
        ver.inc_runtime()
    return response

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/api/sys/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    #core.join()
    log = Log(source=LogSourceType.SERVER.value, types=LogType.LOG.value, msg="Server is down")
    log.save()  
    base.close()
    return 'Server shutting down...'
 
def main():
        #core.start()
    base.connect()
    base.create_tables([Device, Task, Log, ServerVer])
    log = Log.create(source=LogSourceType.SERVER.value, types=LogType.LOG.value, msg="Server is up")
    ver = ServerVer.create(major=1, minor=0, runtime=0)
    app.run()

if __name__ == "__main__":
    main()

# TODO:
#
# 1. system statistics
# 2. device suport (hardcode basic device function)
# 3. add triggering task after each (day, hour, minutes etc.)
# 4. data base optimizations
#
#


