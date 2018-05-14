#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *
from enum import Enum
from datetime import datetime
from croniter import croniter
import json

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

class TaskRespStatusType(Enum):
    Success = 0
    Timeout = 1
    Stopped = 2
    Error   = 3

class DevStatusType(Enum):
    Online  = 0
    Busy    = 1
    Offline = 2
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
        ret = {}
        ret['major']       = self.major
        ret['minor']       = self.minor
        ret['runtime']     = self.runtime
        ret['server_time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return ret

class Device(BaseModel):
    id           = PrimaryKeyField(null=False)
    name         = CharField(null=False)
    lan_address  = CharField(null=False)

    status       = IntegerField(default=DevStatusType.Offline.value)

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
           ServerVer.select().get().inc_runtime()

    def update_online(self, online):
        if self.online != online:
            self.online = online
            self.save()
            ver = ServerVer.select().get()
            ver.inc_runtime()

    def get_json(self):
        ret = {}
        ret['id']           = self.id
        ret['name']         = self.name
        ret['lan_address']  = self.lan_address
        ret['status']       = DevStatusType(self.status).name
        ret['manufacturer'] = self.manufacturer
        ret['device']       = self.device
        ret['serial_num']   = self.serial_num
        ret['firm_ver']     = self.firm_ver
        return ret

class Task(BaseModel):
    name           = CharField(null=False)
    dev            = ForeignKeyField(Device, primary_key=False)
    datetime_begin = DateTimeField(null=True)
    datetime_end   = DateTimeField(null=True)
    cron_str       = CharField(default='* * * * *')
    status         = IntegerField(default=TaskStatusType.Pending.value)
    msg            = TextField(null=False)
    datetime_next  = DateTimeField(null=True)
    series         = BooleanField(default=False)

    def ready_to_execute(self):
        if self.status == TaskStatusType.Pending.value:
            if self.datetime_next is not None:
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
        ret = {}
        ret['name']           = self.name
        ret['id']             = self.id
        ret['dev']            = self.dev.id
        if self.datetime_begin is not None:
            ret['datetime_begin'] = self.datetime_begin.strftime("%d/%m/%Y %H:%M:%S")
        if self.series:
            ret['datetime_end']   = self.datetime_end.strftime("%d/%m/%Y %H:%M:%S")
        ret['cron_str']       = self.cron_str
        ret['status']         = TaskStatusType(self.status).name
        ret['msg']            = self.msg
        if self.datetime_next is not None:
            ret['datetime_next']  = self.datetime_next.strftime("%d/%m/%Y %H:%M:%S")
        ret['series']         = self.series
        return ret

class TaskResp(BaseModel):
    datetime_execute = DateTimeField(default=datetime.now())
    resp             = TextField(default='')
    task             = ForeignKeyField(Task, related_name='responses')
    status           = IntegerField()

    def get_json(self):
        ret = {}
        ret['date_time'] = self.datetime_execute.strftime("%d/%m/%Y %H:%M:%S")
        ret['id']        = self.id
        ret['resp']      = json.loads(self.resp)
        ret['device']    = self.task.dev.name
        ret['task']      = self.task.name
        ret['status']    = TaskRespStatusType(self.status).name
        return ret

class Log(BaseModel):
    date_time = DateTimeField(default=datetime.now)
    source    = IntegerField(null=False)
    types     = IntegerField(null=False)
    msg       = TextField(null=False)

    def get_json(self):
        ret = {}
        ret['date_time'] = self.date_time.strftime("%d/%m/%Y %H:%M:%S")
        ret['id']        = self.id
        ret['source']    = LogSourceType(self.source).name
        ret['types']     = LogType(self.types).name
        ret['msg']       = self.msg
        return ret
