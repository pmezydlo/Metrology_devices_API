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

    def remove_file(self, name):
        os.remove("files/"+name)

    def get_file_info(self):
        ret_file = []
        ret_size = []
        for file in os.listdir("files/"):
            ret_file.append(file)
            ret_size.append(self.bytes_2_human_readable(os.path.getsize(os.path.join("files/", file))))
        ret = [{"name": f, "size": s} for f, s in zip(ret_file, ret_size)]
        return ret

    def get_cpu_info(self):
        number    = []
        usage     = []
        freq_max  = []
        freq_min  = []
        freq_curr = []

        freq  = psutil.cpu_freq(percpu=True)
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

        for i in xrange(psutil.cpu_count()):
            number.append("Cpu"+str(i))
            freq_curr.append(str(freq[i].current)+"MHz")
            freq_min.append(str(freq[i].min)+"MHz")
            freq_max.append(str(freq[i].max)+"MHz")
            usage.append(cpu_usage[i])

        return [{"cpu": cpu, "usage": usage, "min": min, "max": max, "cur": cur} for cpu, usage, min, max, cur in zip(number, usage, freq_min, freq_max, freq_curr)]

    def get_system_information(self):
        json_info = {}
        json_info['system']       = platform.system()
        json_info['proc']         = platform.processor()
        json_info['version']      = platform.version()
        json_info['machine']      = platform.machine()

        json_info['mem_percent']  = str(psutil.virtual_memory().percent)
        json_info['mem_used']     = self.bytes_2_human_readable(psutil.virtual_memory().used)
        json_info['mem_total']    = self.bytes_2_human_readable(psutil.virtual_memory().total)
        json_info['mem_free']     = self.bytes_2_human_readable(psutil.virtual_memory().free)

        json_info['disk_percent'] = str(psutil.disk_usage('/').percent)
        json_info['disk_used']    = self.bytes_2_human_readable(psutil.disk_usage('/').used)
        json_info['disk_total']   = self.bytes_2_human_readable(psutil.disk_usage('/').total)
        json_info['disk_free']    = self.bytes_2_human_readable(psutil.disk_usage('/').free)

        json_info['uptime'] = str(datetime.timedelta(seconds=(int(time.time() - psutil.boot_time()))))
        json_info['boot_time'] = str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%d/%m/%Y %H:%M:%S"))

        json_info['cpu_info'] = self.get_cpu_info()

        return json_info

    def get_ping(self, ip):
        response = os.system("ping -c 1 "+ip)
        if response == 0:
            status = "is up"
        else:
            status = "is down"
        return status
