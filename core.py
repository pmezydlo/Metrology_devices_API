#!/usr/bin/python

import threading
import time
from psql_interface import psql_connection
from device_interface import dev_core

class core(threading.Thread):
    def __init__ (self, base_name, base_user, base_password, base_host):
        threading.Thread.__init__(self)

        self.device_list = []
        self.device_thread_list = []

        self.base = psql_connection(base_name, base_user, base_password, base_host)

    def run(self):
        def get_device_list():
            self.device_list = self.base.get_device_list()

        def add_new_device():
            for row_device_list in self.device_list:
                # if want to add new device 
                    dev = dev_core(row_device_list["id"], row_device_list["own_name"], row_device_list["lan_address"], row_device_list["lan_port"])  
                    self.device_thread_list.append(dev)
                    dev.start()

        def ping_device():
            pass
            
        def print_device_list():
             for row_device_list in self.device_list:
                print row_device_list["own_name"]

        def core_release():
            for dev_thread in self.device_thread_list:
                dev_thread.join()

            self.base.psql_disconnect()
        
        get_device_list()
        add_new_device()
        # the main thread loop
        counter = 4
        while counter:
            print counter

            get_device_list()

            print_device_list()

            time.sleep(1)
            counter -= 1

        core_release()

def main():
    name = "measure_device_base"
    user = "postgres"
    password = "postgres"
    host = "localhost"

    c = core(name, user, password, host)
    c.start()
    c.join()

if __name__ == "__main__":
    main()
