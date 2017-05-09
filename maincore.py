#!/usr/bin/python

from psql_interface import psql_connection
import datetime
import sys
import threading
from telnetlib_receive_all import Telnet
import time
import Queue
from enum import Enum

class PART_SYS(Enum):
    CORE = 1
    BASE = 2
    TASK = 3

rqs_queue = Queue.Queue()

class lan(object):
    def __init__(self, lan_ip, lan_port):
        try:
            self.lan_port = lan_port
            self.lan_ip = lan_ip
            self.tn = Telnet(lan_ip, lan_port) 
        except:
            print('lan error')

    def read(self, command):
        wait = 2
        response = ""
        while response != "2\n":
            self.tn.write("*OPC?\n")
            response = self.tn.read_until("\n", wait)

        self.tn.write(command + "\n")
        return self.tn.read_until("\n", wait)

    def write(self, command):
        self.tn.write(command + "\n")

    def ping(self):
        return os.system("ping -c 2 " + osc_ip + " > /dev/null")

    def close(self):
        self.tn.close()

class task_core (threading.Thread):
    def __init__ (self, task_id, task_name, lan_ip, lan_port):
        threading.Thread.__init__(self)

        self.id = task_id
        self.name = task_name

        self.rqss_queue = rqs_queue 
        
        self.lan_ip = lan_ip
        self.lan_port = lan_port
        #self.dev = lan(self.lan_ip, self.lan_port)
        self.msg_queue = Queue.Queue()

    def run(self):
        while not self.msg_queue.empty():
            rqs_data = []
            rqs_data.append(PART_SYS.BASE)
            rqs_data.append(self.id)
            rqs_data.append(self.msg_queue.get())
            self.rqss_queue.put(rqs_data)
        rqs_data = []
        rqs_data.append(PART_SYS.CORE)
        rqs_data.append(self.id)
        rqs_data.append('END')
        self.rqss_queue.put(rqs_data)

class maincore(threading.Thread):
    def __init__ (self, base_name, base_user, base_password, base_host):
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
                task_thread = 0
                try:
                    dev = self.base.get_device_by_id(task["dev"])
                    task_thread = task_core(task["id"], task["name"], dev[0]["lan_address"], dev[0]["lan_port"]) 
                    
                    msgs = task["msg"].splitlines() 
                    for msg in msgs:
                        task_thread.msg_queue.put(msg)

                    task_thread.start()
                except:
                    print "register new thread error"
                else:
                    print "register thread ok"
                    self.tasks_thread_list.append(task_thread)
                    self.base.update_task_status(task["id"], 'RUN')

        def delete_thread_task(task_id):
            for task_th in self.tasks_thread_list:
                if (task_id == task_th.id):
                    task_th.join()
                    self.tasks_thread_list.remove(task_th)

        def core_release():
            for task_th in self.tasks_thread_list:
                task_th.join()
                del(task_th)
            self.base.psql_disconnect()

        def push_task_request(task_id, msgs):
            task_msg = self.base.get_task_request(task_id)
            self.base.push_task_request(task_id, '{}\n{}'.format(task_msg, msgs))

        add_tasks_to_execute()
        counter = 5
        while counter:
            print counter 
            time.sleep(0.5)
            counter -= 1

        while not rqs_queue.empty():
            data = rqs_queue.get()
            if (data[0] == PART_SYS.CORE):
                if (data[2] == 'END'):
                    self.base.update_task_status(data[1], 'READY')
                    delete_thread_task(data[1])

            elif (data[0] == PART_SYS.BASE):
                push_task_request(data[1], data[2])
            else:
                print "error"
                
        core_release()
