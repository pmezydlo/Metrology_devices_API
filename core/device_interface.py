import sys
from telnetlib_receive_all import Telnet

class lan(object):
    def __init__(self, lan_ip, lan_port):
        try:
            self.lan_port = lan_port
            self.lan_ip = lan_ip
            self.tn = Telnet(lan_ip, lan_port) 
        except:
            print('lan error')
            sys.exit("ERROR")

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

class dev_core (threading.Thread):
    def __init__ (self, threadID, dev_id, own_dev_name, lan_ip, lan_port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.dev = None
        self.name = own_dev_name
        self.dev_id = dev_id
        self.lan_ip = lan_ip
        self.lan_port = lan_port
        self.dev = lan(self.lan_ip, self.lan_port)

    def dev_run(self):
        counter = 5
        delay = self.threadID;
        while counter:
            print threadID 
            id = self.dev.read("*IDN?")

            if id == "command_error":
                print('No response from device')
                sys.exit("ERROR")

            ids = id.split(',')
    
            print ids

            self.manufacturer = ids[0]
            self.dev_name = ids[1]
            self.serial_number = ids[2]
            self.firmware_version = ids[3]
            time.sleep(delay)
            counter -= 1

    def dev_exit():
        pass
