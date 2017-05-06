#!/usr/bin/python

import threading
import time
from psql_interface import psql_connection
from device_interface import dev_core

class maincore(threading.Thread):
    def __init__ (self, base_name, base_user, base_password, base_host):
        threading.Thread.__init__(self)

        self.devices_thread_list = []
        self.base = psql_connection(base_name, base_user, base_host, base_password)

    def run(self):
        def add_new_device():
            dev_list = self.base.get_noready_device_list()
            for dev in dev_list:
                dev_thread = 0
                print dev["status"]
                try:
                    dev_thread = dev_core(dev["id"], dev["own_name"], dev["lan_address"], dev["lan_port"]) 
                    dev_thread.start()
                except:
                    print "register new thread error"
                else:
                    print "register thread ok"
                    self.devices_thread_list.append(dev_thread)
                    self.base.update_device_status(dev["id"], 'READY')

        def core_release():
            for dev_th in self.devices_thread_list:
                dev_th.join()
            self.base.psql_disconnect()

        add_new_device()
        core_release()
        counter = 1
        while counter:
            time.sleep(1)
            print counter
            counter -= 1

