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

import threading
from base_interface import *
import vxi11
import time
from entry_points import *
import json
import socket

class task_core(threading.Thread):
    def __init__(self, task, dev):
        threading.Thread.__init__(self)
        self.dev = dev
        self.task = task
        
        self.end_flag  = False
        self.stop_flag = False

        self.instr = vxi11.Instrument(self.dev.lan_address)
        self.ret_msg = []
        self.ret_res = []
        self.status = TaskRespStatusType.Success

    def run(self):
        def is_entry_point(line):
            arg = line[line.find("(")+1:line.find(")")]
            name = line.split('(', 1)[0]
    
            if name in entry_array:
                return True
            else:
                return False

        def parse_cmds(line):
            # IEEE488.2 common commands or SCPI commands
            if line[0] == '*' or line[0] == ':':
                # command is query
                if line[-1] == '?':
                    try:
                        ret = self.instr.ask(line)
                    except vxi11.vxi11.Vxi11Exception as e:
                        ret = str(e)
                    except socket.error as e:
                        ret = str(e)
                # or is anything else
                else:
                    try:
                        self.instr.write(line)
                    except vxi11.vxi11.Vxi11Exception as e:
                        ret = str(e)
                    else:
                        ret = 'ok'

            # entry point
            elif is_entry_point(line):
                arg = line[line.find("(")+1:line.find(")")]
                name = line.split('(', 1)[0]
                ret = entry_array[name](self.instr, arg)

            # not defined
            else:
                ret = 'Invalid command'

            self.ret_msg.append(line)
            self.ret_res.append(ret)

        def execute_cmds():
            lines = self.task.msg.splitlines()
            for line in lines:
                parse_cmds(line)
                if self.stop_flag:
                    self.status = TaskRespStatusType.Stopped
                    break

        def check_connection():
            try:
                self.instr.ask("*OPC?")
                self.task.dev.update_status(DevStatusType.Busy.value)             
                return True
            except vxi11.vxi11.Vxi11Exception as e:
                self.status = TaskRespStatusType.Timeout
                self.task.dev.update_status(DevStatusType.Offline.value)
                return False
            except socket.error as e:
                self.status = TaskRespStatusType.Error
                self.task.dev.update_status(DevStatusType.Error.value)
                return False

    #    print "execute"
    #    print(self.task.name)
        if check_connection():
            execute_cmds()
            self.task.dev.update_status(DevStatusType.Online.value)
     
        self.response = [{"msg": m, "resp": r} for m, r in zip(self.ret_msg, self.ret_res)]
        self.end_flag = True
        
class maincore(threading.Thread): 
    def __init__(self):
        threading.Thread.__init__(self)
        self.exit_signal = False
        self.tasks_thread_list = []
        self.detect = False
        self.check_conn = False
        self.dev_id     = 0

    def run(self):
        def check_dev_connection():
            print("check_dev_connection - start")
            query = Device.select().where(Device.id == self.dev_id)
            if query:
                dev = query.get()
                instr = vxi11.Instrument(dev.lan_address)
            try:
                Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="Connection with {} device checking was started".format(dev.name))
                instr.ask("*OPC?")
            except vxi11.vxi11.Vxi11Exception as e:
                dev.update_status(DevStatusType.Error.value)
            except socket.error as e:
                dev.update_status(DevStatusType.Offline.value)
            else:
                dev.update_status(DevStatusType.Online.value)

        def get_device_info(dev):
            instr = vxi11.Instrument(dev.lan_address)
            instr.open()
            dev.update_info(instr.ask("*IDN?"))
            instr.close()

        def detect_devices():
            list_of_dev = vxi11.list_devices()
            for dev in list_of_dev:
                query = Device.select().where(Device.lan_address == dev)
                if not query.exists():
                    new_dev = Device.create(name="device", lan_address=dev)
                    get_device_info(new_dev)
                    Log.create(source=LogSourceType.Server.value, types=LogType.Info.value, msg="{} device was added by auto-detection".format(new_dev.name))
                    ServerVer.select().get().inc_runtime()

        def delete_task_thread():
            for task in self.tasks_thread_list:
                if task.end_flag:
                    task.task.update_status(TaskStatusType.Ready.value)


               #     print "task was released"
                    resp = TaskResp.create(resp=json.dumps(task.response), task=task.task, status=task.status.value)
              #      print resp.resp
                    task.join()
                    self.tasks_thread_list.remove(task)
                    Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg=task.task.name+" task was executed")
                    ServerVer.select().get().inc_runtime()

        def get_tasks_to_execute():
            for task in Task.select():
                if task.ready_to_execute():
                    print("get_tasks_to_execute()")
                    task.update_status(TaskStatusType.Run.value)
                    task_thread = task_core(task, task.dev)
                    task.dev.update_status(DevStatusType.Busy.value)
                    self.tasks_thread_list.append(task_thread)
                    task_thread.start()
                    Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg=task.name+" task has began")
                    ServerVer.select().get().inc_runtime()

        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is up")
        while not self.exit_signal:
            get_tasks_to_execute()
            delete_task_thread()
            if self.detect:
                self.detect = False
                detect_devices()
            if self.check_conn:
                self.check_conn = False
                check_dev_connection()

        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is down")
