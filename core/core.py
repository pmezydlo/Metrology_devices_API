import Queue
import threading

from psql_interface import psql_connection
from device_interface import device_core

base = psql_connection("measure_device_base", "postgres", "postgres", "localhost")

device_list = base.get_device_list()

device_thread_list = []

thread_id = 0;
for row_device_list in device_list:
    thread_id++
    dev = dev_core(thread_id, row_device_list["id"], row_device_list["own_name"], row_device_list["lan_address"], row_device_list["lan_port"]) 
    device_thread_list.append(dev)

for dev_thread in row_device_list:
    dev_thread.join()

base.psql_disconnect()
