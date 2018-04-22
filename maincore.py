#!/usr/bin/python
import threading
from base_interface import *

class maincore(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exit_signal = False
        
    def run(self):
        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is up")
        while (self.exit_signal == False):
            for task in Task.select():
                if task.ready_to_execute() == True:
                    task.update_status(TaskStatusType.Run.value)
                    print task.name
                    print "execute"
                    task.update_status(TaskStatusType.Ready.value)

                
        Log.create(source=LogSourceType.Core.value, types=LogType.Info.value, msg="Core is down")
