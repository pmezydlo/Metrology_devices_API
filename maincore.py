#!/usr/bin/python

import threading
import time
from psql_interface import psql_connection
from device_interface import dev_core

#class maincore(threading.Thread):
 #   def __init__ (self, base_name, base_user, base_password, base_host):
  #      threading.Thread.__init__(self)

   #     self.devices_list = []
    #    self.status = 0
     #   self.base = psql_connection(base_name, base_user, base_host, base_password)

    #def run(self):
  #      def add_new_device():
            
                
                # if want to add new device 
   #             psql_id = 2
    #            dev = dev_core(row_device_list["id"], row_device_list["own_name"], row_device_list["lan_address"], row_device_list["lan_port"]) 
     #           dev_s = DevStruct(psql_id, 'register', dev_core
                
                # 
                #self.device_thread_list.append(dev)
                #dev.start()
            
      #  def print_device_list():
       #      for dev in devices_list:
            #    dev.dev

        #def core_release():
         #   for dev in devices_list:
          #      dev.dev_core.join()

           # self.base.psql_disconnect()
        
     #   counter = 50
      #  while counter:
       #     time.sleep(1)
        #    counter -= 1
         #   print counter
          #  print self.status
            
       # core_release()


class maincore(threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.status = 1

    def run(self):      
        while (self.status == 1):
            time.sleep(1)
            print self.status

