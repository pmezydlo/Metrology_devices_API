#!/usr/bin/python
import threading
from base_interface import *

class maincore(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exit_signal = False
        self.tasks_thread_list = []
        
    def run(self):
        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is up")
        while (self.exit_signal == False):
            for task in Task.select():
                if task.get_to_execute:
                    print "execute"
                
        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is down")
