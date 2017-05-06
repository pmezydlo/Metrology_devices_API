import sys
import threading
from telnetlib_receive_all import Telnet
import time
import Queue

class lan(object):
    def __init__(self, lan_ip, lan_port):
        try:
            self.lan_port = lan_port
            self.lan_ip = lan_ip
            self.tn = Telnet(lan_ip, lan_port) 
        except:
            print('lan error')

    def read(self, command):
        wait = 1
        response = ""
        while response != "1\n":
            self.tn.write("*OPC?\n")
            response = self.tn.read_until("\n", wait)

        self.tn.write(command + "\n")
        return self.tn.read_until("\n", wait)

    def write(self, command):
        self.tn.write(command + "\n")

    def ping(self):
        return os.system("ping -c 1 " + osc_ip + " > /dev/null")

    def close(self):
        self.tn.close()

class task_core (threading.Thread):
    def __init__ (self, task_id, task_name, lan_ip, lan_port):
        threading.Thread.__init__(self)

        self.name = task_name
        
        self.lan_ip = lan_ip
        self.lan_port = lan_port
        #self.dev = lan(self.lan_ip, self.lan_port)
        self.msg_queue = Queue.Queue()

    def run(self):
        print self.name
        #while not self.msg_queue.empty():
          #  print self.msg_queue.get()

