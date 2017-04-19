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

class device(object):
    def __init__ (self, *argv): 
        arg_len = len(argv)
        self.con_type = argv[0]
        self.dev = None

        if self.con_type == "usb":
            if arg_len == 2:
                self.usb_path = argv[1]
                self.dev = usb(self.usb_path)
            else:
                print('bad arg list')
                sys.exit("ERROR")

        elif self.con_type == "lan":
            if arg_len == 3:
                self.lan_ip = argv[1]
                self.lan_port = argv[2]
                self.dev = lan(self.lan_ip, self.lan_port)
            else:
                print('bad arg list')
                sys.exit("ERROR")

        elif self.con_type == "rs232":
            if arg_len == 4:
                self.rs232_port = argv[1]
                self.rs232_baudrate = argv[2]
                self.rs232_timeout = argv[3]
                self.dev = rs232(self.rs232_port, self.rs232_baudrate, self.rs232_timeout)
            else:
                print('bad arg list')
                sys.exit("ERROR");
        else:
            print('bad arg list')
 
        id = self.dev.read("*IDN?")

        if id == "command_error":
            print('No response from device')
            sys.exit("ERROR")

        ids = id.split(',')

        self.manufacturer = ids[0]
        self.dev_name = ids[1]
        self.serial_number = ids[2]
        self.firmware_version = ids[3]

    def write(self, command):
        self.dev.write(command)

    def read(self, command):
        return self.dev.read(command)

    def close(self):
        self.dev.close()

