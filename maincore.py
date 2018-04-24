#!/usr/bin/python
import threading
from base_interface import *
import vxi11
import time


class device_thread(threading.Thread):
    def __init__(self):
        self.busy_flag = False
        self.exit_signal = False

    def check_connection(self):
        pass

    def run(self):
        pass

class maincore(threading.Thread): 
    def __init__(self):
        threading.Thread.__init__(self)
        self.exit_signal = False
        self.device_thread_list = []


        self.instr =  vxi11.Instrument("TCPIP::192.168.0.207::INSTR")
        

    def get_tasks_to_execute(self):  
        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is up")
        while (self.exit_signal == False):
            for task in Task.select():
                if task.ready_to_execute() == True:
                    task.update_status(TaskStatusType.Run.value)
                    print task.name
                    print "execute"
                    task.update_status(TaskStatusType.Ready.value)
        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is down")

    def run(self):
        while (self.exit_signal == False):
            for dev in Device.select():
                dev.name
                try:
                    dev.update_info(self.instr.ask("*IDN?"))
                except:
                    dev.update_online(False)
                else:
                    dev.update_online(True)
               
            time.sleep(1)
