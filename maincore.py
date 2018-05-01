#!/usr/bin/python
import threading
from base_interface import *
import vxi11
import time

class task_core(threading.Thread):
    def __init__(self, task, dev):
        threading.Thread.__init__(self)
        self.dev = dev
        self.task = task
        self.ready_flag = False
        self.instr = vxi11.Instrument(self.dev.lan_address)

    def run(self):
        def parse_and_execute_cmds():
            lines = self.task.msg.splitlines()
            for line in lines:
                print line
        
        self.task.update_status(TaskStatusType.Run.value)
        print "execute"
        print self.dev.name
        print self.task.name
        print self.task.status
        print self.instr.ask("*IDN?")
        parse_and_execute_cmds()
        self.task.update_status(TaskStatusType.Ready.value)
        self.ready_flag = True
        
class maincore(threading.Thread): 
    def __init__(self):
        threading.Thread.__init__(self)
        self.exit_signal = False
        self.tasks_thread_list = []

    def run(self):
        def get_devices_status():
            for dev in Device.select():
                dev.name
                try:
                    dev.update_info(self.instr.ask("*IDN?"))
                except:
                    dev.update_online(False)
                else:
                    dev.update_online(True)

        def delete_task_thread():
            for task in self.tasks_thread_list:
                if task.ready_flag == True:
                    print "task was released"
                    task.join()
                    self.tasks_thread_list.remove(task)



        def get_tasks_to_execute():  
            for task in Task.select():
                if task.ready_to_execute() == True:

                    task_thread = task_core(task, task.dev)
                    self.tasks_thread_list.append(task_thread)
                    task_thread.start()

            time.sleep(1);

        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is up")
        while (self.exit_signal == False):
            get_tasks_to_execute()
            delete_task_thread()
        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is down")
