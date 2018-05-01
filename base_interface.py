#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *
from enum import Enum
from datetime import datetime
from croniter import croniter

base = SqliteDatabase('MDA.db')

class LogType(Enum):
    Info    = 0
    Warning = 1
    Error   = 2

class LogSourceType(Enum):
    Task        = 0
    Core        = 1
    Base        = 2
    NotDefined  = 3
    Server      = 4

class TaskStatusType(Enum):
    Pending = 0
    Run     = 1
    Ready   = 2
    Error   = 3

class BaseModel(Model):
    class Meta:
        database = base

class ServerVer(BaseModel):
    major    = IntegerField(null=False)
    minor    = IntegerField(null=False)
    runtime  = IntegerField(default=0)

    def inc_runtime(self):
        self.runtime += 1
        self.save()

    def get_json(self):
        datetime_str = datetime.now()
        return ({"major":self.major,
                 "minor":self.minor,
                 "runtime":self.runtime,
                 "server_time":datetime_str.strftime("%Y-%m-%d %H:%M:%S")})

class Device(BaseModel):
    id          = PrimaryKeyField(null=False)
    name        = CharField(null=False)
    lan_address = CharField(null=False)

    online       = BooleanField(default=False)
    manufacturer = CharField(default="")
    device       = CharField(default="")
    serial_num   = CharField(default="")
    firm_ver     = CharField(default="")

    def update_info(self, idn_str):
       idn_str_split = idn_str.split(",")
       if idn_str_split[0] != self.manufacturer or idn_str_split[1] != self.device or idn_str_split[2] != self.serial_num or idn_str_split[3] != self.firm_ver:
           self.manufacturer = idn_str_split[0]
           self.device       = idn_str_split[1]
           self.serial_num   = idn_str_split[2]
           self.firm_ver     = idn_str_split[3]
           self.save()
           ver = ServerVer.select().get()
           ver.inc_runtime()

    def update_online(self, online):
        if self.online != online:
            self.online = online
            self.save()
            ver = ServerVer.select().get()
            ver.inc_runtime()

    def get_json(self):
        return ({"id":self.id,
                 "name":self.name,
                 "lan_address":self.lan_address,
                 "online":self.online,
                 "manufacturer":self.manufacturer,
                 "device":self.device,
                 "serial_num":self.serial_num,
                 "firm_ver":self.firm_ver
                 })

class TaskRep(BaseModel):
    datetime_execute = DateTimeField(default=datetime.now())
    rep              = TextField(default='')

class Task(BaseModel):
    name           = CharField(null=False)
    dev            = ForeignKeyField(Device, primary_key=False)
    datetime_begin = DateTimeField(null=True)
    datetime_end   = DateTimeField(null=True)
    cron_str       = CharField(default='* * * * *')
    status         = IntegerField(default=TaskStatusType.Pending.value)
    msg            = TextField(null=False)
    rep            = ForeignKeyField(TaskRep, related_name='replies', null=True)
    datetime_next  = DateTimeField(null=True)
    series         = BooleanField(default=False)

    def ready_to_execute(self):
        if self.status == TaskStatusType.Pending.value:
            if self.datetime_next < datetime.now():
                if self.series == True:
                    iter  = croniter(self.cron_str, self.datetime_next) 
                    self.datetime_next = iter.get_next(datetime)
                    return True
                else:
                    return True
            else:
                return False
        else:
            return False

    def update_status(self, state):
        if state == TaskStatusType.Run.value:
            self.status = TaskStatusType.Run.value
        elif state == TaskStatusType.Ready.value:
            if self.series == False:
                self.status = TaskStatusType.Ready.value
            else:
                if self.datetime_end < self.datetime_next:
                    self.status = TaskStatusType.Ready.value
                else:
                    self.status = TaskStatusType.Pending.value
        else:
            self.status = TaskStatusType.Error.value
        self.save()

    def get_json(self):
        return 'ok''''({"name":self.name,
                 "id":self.id,
                 "dev_name":self.dev.name,

                 "date_begin":self.date_begin,
                 "date_end":self.date_end,

                 "time_begin":self.time_begin,
                 "time_end":self.time.end,

                 "minutes":self.minutes,
                 "hours":self.hours,
                 "month_days":self.month_days,
                 "months":self.months,
                 "week_days":week_days,

                 "status":TaskStatusType(self.status).name,
                 "msg":self.msg)}
'''

class Log(BaseModel):
    date_time = DateTimeField(default=datetime.now)
    source    = IntegerField(null=False)
    types     = IntegerField(null=False)
    msg       = TextField(null=False)

    def get_json(self):
        return ({"date_time":self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                 "id":self.id,
                 "source":LogSourceType(self.source).name,
                 "types":LogType(self.types).name,
                 "msg":self.msg})
