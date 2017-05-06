#!/usr/bin/python

import threading
import time
from psql_interface import psql_connection
from task_interface import task_core
import datetime

class maincore(threading.Thread):
    def __init__ (self, base_name, base_user, base_password, base_host):
        threading.Thread.__init__(self)

        self.tasks_thread_list = []
        self.base = psql_connection(base_name, base_user, base_host, base_password)

    def run(self):
        def add_task_to_execute():
            dt = datetime.datetime.now()
            d = dt.strftime("%d.%m.%y")
            t = dt.strftime("%H:%M:%S")
            task_list = self.base.get_pending_task(d, t)
            print task_list
            print d
            print t
            print "==========="
            for task in task_list:
                task_thread = 0
                print task["status"]
                try:
                    dev = self.base.get_device_by_id(task["dev"])
                    task_thread = task_core(task["id"], task["name"], dev[0]["lan_address"], dev[0]["lan_port"]) 
                    task_thread.start()
                except:
                    print "register new thread error"
                else:
                    print "register thread ok"
                    self.tasks_thread_list.append(task_thread)
                    self.base.update_task_status(task["id"], 'RUN')

        def core_release():
            for task_th in self.tasks_thread_list:
                task_th.join()
            self.base.psql_disconnect()

        #add_new_device()
        #transmit_task()
        #core_release()

        counter = 400
        while counter:
            add_task_to_execute()           
            #print('{}.{}.{}'.format(dt.day, dt.month, dt.year))
            #print dt.hour + ":" + dt.minute + ":" + dt.second
            time.sleep(0.5)
            counter -= 1

