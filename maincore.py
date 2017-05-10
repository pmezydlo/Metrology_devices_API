#!/usr/bin/python

from psql_interface import psql_connection
import datetime
import threading
from telnetlib_receive_all import Telnet
import time
import Queue
from enum import Enum

class PART_SYS(Enum):
    CORE = 1
    BASE = 2
    TASK = 3
    LOGS = 4

class msg(object):
    def __init__(self, owner, owner_id, receiver, receiver_id, data):
        self.owner = owner
        self.owner_id = owner_id
        self.receiver = receiver
        self.receiver_id = receiver_id
        self.data = data

rqs_queue = Queue.Queue()

class task_core(threading.Thread):
    def __init__(self, task_id, task_name, lan_ip, lan_port):
        threading.Thread.__init__(self)
        self.id = task_id
        self.name = task_name
        self.rqss_queue = rqs_queue
        self.lan_port = lan_port
        self.lan_ip = lan_ip      
        self.cmd_queue = Queue.Queue()
            
    def run(self): 
        def push_log_msg(type_log, msg_log):
            log_msg = msg(PART_SYS.TASK, self.id, PART_SYS.LOGS, 0, "{}|{}".format(type_log, msg_log))
            self.rqss_queue.put(log_msg)

        def lan_connect(lan_ip, lan_port):
            try:
                self.tn = Telnet(lan_ip, lan_port) 
            except:
                push_log_msg('ERROR', "lan ip:{} connection failed".format(lan_ip))
            else:
                push_log_msg('LOG', "lan ip:{} connecting is ready".format(lan_ip))

        def lan_read(command):
            wait = 2
            response = ""
            while response != "1\n":
                self.tn.write("*OPC?\n")
                response = self.tn.read_until("\n", wait)

            self.tn.write(command + "\n")
            return self.tn.read_until("\n", wait)

        def lan_write(command):
            wait = 2
            self.tn.write(command + "\n")
            response = ""
            while response != "1\n":
                self.tn.write("*OPC?\n")
                response = self.tn.read_until("\n", wait)

        def lan_close():
            self.tn.close()
           
        def get_task_to_execute():
            while not self.cmd_queue.empty():
                data = self.cmd_queue.get()
                cmd = data.data.split('|')
                ret = 0
                if cmd[0] == 'W':
                    lan_write(cmd[1])
                    ret = 'ok\n'
                elif cmd[0] == 'R':
                    ret = lan_read(cmd[1])

                rqs_data = msg(PART_SYS.TASK, self.id, PART_SYS.BASE, 0, ret)
                self.rqss_queue.put(rqs_data)

        lan_connect(self.lan_ip, self.lan_port)
        get_task_to_execute()
        lan_close()

        rqs_data = msg(PART_SYS.TASK, self.id, PART_SYS.CORE, 0, 'END')
        self.rqss_queue.put(rqs_data)

class maincore(threading.Thread):
    def __init__(self, base_name, base_user, base_password, base_host):
        threading.Thread.__init__(self)
        self.tasks_thread_list = []
        self.base = psql_connection(base_name, base_user, base_host, base_password)

    def run(self):
        def add_tasks_to_execute():
            dt = datetime.datetime.now()
            d = dt.strftime("%d.%m.%y")
            t = dt.strftime("%H:%M:%S")
            task_list = self.base.get_pending_task(d, t)
            for task in task_list:
                try:
                    dev = self.base.get_device_by_id(task["dev"])
                    task_thread = task_core(task["id"], task["name"], dev[0]["lan_address"], dev[0]["lan_port"]) 
                    lines = task["msg"].splitlines()
                    for line in lines:
                        cmd = msg(PART_SYS.CORE, 0, PART_SYS.TASK, task["id"], line)
                        task_thread.cmd_queue.put(cmd)

                    task_thread.start()
                except:
                    self.base.push_log_msg('CORE', 'ERROR', "Core has problem with register new thread")
                else:
                    self.base.push_log_msg('CORE', 'LOG', "TASK id:{} name:{} ruinning correctly".format(task["id"], task["name"]))
                    self.tasks_thread_list.append(task_thread)
                    self.base.update_task_status(task["id"], 'RUN')

        def delete_thread_task(task_id):
            for task_th in self.tasks_thread_list:
                if task_id == task_th.id:
                    task_th.join()
                    self.tasks_thread_list.remove(task_th)

        def core_release():
            for task_th in self.tasks_thread_list:
                task_th.join()
            self.base.push_log_msg('CORE', 'LOG', "Core has ended")
            self.base.psql_disconnect()

        def discharge_rqs_queue():
            while not rqs_queue.empty():
                rqs = rqs_queue.get()
                if rqs.receiver == PART_SYS.CORE:
                    if rqs.data == 'END':
                        self.base.update_task_status(rqs.owner_id, 'READY')
                        self.base.push_log_msg('CORE', 'LOG', "TASK id:{} has ended".format(rqs.owner_id))
                        delete_thread_task(rqs.owner_id)
           
                elif rqs.receiver == PART_SYS.LOGS:
                    msgs = rqs.data.split("|")
                    self.base.push_log_msg('TASK', msgs[0], msgs[1])

                elif rqs.receiver == PART_SYS.BASE:
                    old_rqs = self.base.get_task_request(rqs.owner_id)
                    self.base.push_task_request(rqs.owner_id, '{}{}'.format(old_rqs, rqs.data))
                else:
                    self.base.push_log_msg('CORE', 'LOG', "Core have problem with interpreting tasks request")

        counter = 600
        while counter:
            add_tasks_to_execute() 
            time.sleep(0.1)
            counter -= 1
            discharge_rqs_queue()

        core_release()
