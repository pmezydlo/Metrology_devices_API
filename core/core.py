#!/usr/bin/python

import threading
import thread
import time
from psql_interface import psql_connection
from device_interface import dev_core

def add_new_device_thread(device_list):
    device_list_to_add = base.get_device_list()

    for dev in device_list:
        device_list_to_add.remove(dev["id"]);

    for dev in device_list_to_add:
        print dev["id"]

    while 1:
        print "check new device"
        time.sleep(0.5);

base = psql_connection("measure_device_base", "postgres", "postgres", "localhost")

device_list = []

device_thread_list = []

for row_device_list in device_list:
    dev = dev_core(row_device_list["id"], row_device_list["own_name"], row_device_list["lan_address"], row_device_list["lan_port"])  
    device_thread_list.append(dev)
    dev.start()

thread.start_new_thread(add_new_device_thread, ())
print "base release"
base.psql_disconnect()

for dev_thread in device_thread_list:
    dev_thread.join()



