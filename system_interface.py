import sys
import json
import datetime
import platform
import psutil
import os

class system_interface(object):
    def __init__ (self):
        pass

    def bytes_2_human_readable(self, number_of_bytes):
        step_to_greater_unit = 1024.

        number_of_bytes = float(number_of_bytes)
        unit = 'bytes'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'KB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'MB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'GB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'TB'

        precision = 1
        number_of_bytes = round(number_of_bytes, precision)

        return str(number_of_bytes) + ' ' + unit

    def get_system_information(self):
        json_info = {}
        json_info['system']  = platform.system()
        json_info['proc']    = platform.processor()
        json_info['version'] = platform.version()
        json_info['machine'] = platform.machine()

        json_info['mem_percent'] = str(psutil.virtual_memory().percent)+'%'
        json_info['mem_used']    = self.bytes_2_human_readable(psutil.virtual_memory().used)
        json_info['mem_total']   = self.bytes_2_human_readable(psutil.virtual_memory().total)
        json_info['mem_free']    = self.bytes_2_human_readable(psutil.virtual_memory().free)

        json_info['disk_percent'] = str(psutil.disk_usage('/').percent)+'%'
        json_info['disk_used']    = self.bytes_2_human_readable(psutil.disk_usage('/').used)
        json_info['disk_total']   = self.bytes_2_human_readable(psutil.disk_usage('/').total)
        json_info['disk_free']    = self.bytes_2_human_readable(psutil.disk_usage('/').free)

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

        return json.dumps(json_info)

    def get_ping(self, ip):
        response = os.system("ping -c 1 "+ip)
        if response == 0:
            status = "is up"
        else:
            status = "is down"
        return status


