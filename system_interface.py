import sys
import json
import datetime
import platform
import psutil
import os
import time

class system_interface(object):
    def __init__ (self):
        pass

    def bytes_2_human_readable(self, n):
        symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

    def get_file_info(self):
        ret_file = []
        ret_size = []
        for file in os.listdir("files/"):
            ret_file.append(file)
            ret_size.append(self.bytes_2_human_readable(os.path.getsize(os.path.join("files/", file))))
        ret = [{"name": f, "size": s} for f, s in zip(ret_file, ret_size)]
        return ret

    def get_system_information(self):
        json_info = {}
        json_info['system']  = platform.system()
        json_info['proc']    = platform.processor()
        json_info['version'] = platform.version()
        json_info['machine'] = platform.machine()

        json_info['mem_percent'] = str(psutil.virtual_memory().percent)
        json_info['mem_used']    = self.bytes_2_human_readable(psutil.virtual_memory().used)
        json_info['mem_total']   = self.bytes_2_human_readable(psutil.virtual_memory().total)
        json_info['mem_free']    = self.bytes_2_human_readable(psutil.virtual_memory().free)

        json_info['disk_percent'] = str(psutil.disk_usage('/').percent)
        json_info['disk_used']    = self.bytes_2_human_readable(psutil.disk_usage('/').used)
        json_info['disk_total']   = self.bytes_2_human_readable(psutil.disk_usage('/').total)
        json_info['disk_free']    = self.bytes_2_human_readable(psutil.disk_usage('/').free)

        json_info['uptime'] = str(datetime.timedelta(seconds=(int(time.time() - psutil.boot_time()))))
        json_info['boot_time'] = str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))


        cpu_usage = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_usage_str = ""
        for i in xrange(len(cpu_usage)):
            cpu_usage_str+="Cpu"+str(i)+":"+str(cpu_usage[i])+"%"+'\n'

        json_info['cpu_usage'] = cpu_usage_str

        cpu_min_str = ""
        cpu_max_str = ""
        cpu_freq_str = ""

        cpu_freq = psutil.cpu_freq(percpu=True)
        for i in xrange(len(cpu_freq)):
            cpu_max_str += "Cpu"+str(i)+": " + str(cpu_freq[i].max) + "MHz "
            cpu_min_str += "Cpu"+str(i)+": " + str(cpu_freq[i].min) + "MHz "
            cpu_freq_str += "Cpu"+str(i)+": " + str(cpu_freq[i].current) + "MHz "

        json_info['cpu_freq_max'] = cpu_max_str
        json_info['cpu_freq_min'] = cpu_min_str
        json_info['cpu_freq_curr'] = cpu_freq_str
        json_info['user_files'] = self.get_file_info()
        return json.dumps(json_info)

    def get_ping(self, ip):
        response = os.system("ping -c 1 "+ip)
        if response == 0:
            status = "is up"
        else:
            status = "is down"
        return status

