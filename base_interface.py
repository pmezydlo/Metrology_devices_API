#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *
from enum import Enum
from datetime import *

base = SqliteDatabase('MDA.db')

class DeviceType(Enum):
    NOT_DEFINED        = 0
    OSCILLOSCOPE       = 1
    MULTIMETER         = 2
    FUNCTION_GENERATOR = 3

class LogType(Enum):
    LOG     = 0
    WARNING = 1
    ERROR   = 2

class LogSourceType(Enum):
    TASK        = 0
    CORE        = 1
    BASE        = 2
    NOT_DEFINED = 3
    SERVER      = 4

class TaskStatusType(Enum):
    PENDING = 0
    RUN     = 1
    READY   = 2

class BaseModel(Model):
    class Meta:
        database = base

class Device(BaseModel):
    id          = PrimaryKeyField(null=False)
    name        = CharField(null=False)
    types       = IntegerField(null=False)
    lan_address = CharField(null=False)
    lan_port    = IntegerField(default=5555)
    ps_channel  = IntegerField(default=0)

class Task(BaseModel):
    name   = CharField(null=False)
    dev    = ForeignKeyField(Device, primary_key=False)
    date   = CharField(null=False)
    time   = CharField(null=False)
    status = IntegerField(null=False)
    msg    = TextField(default='')
    req    = TextField(default='')

class Log(BaseModel):
    date_time = DateTimeField(default=datetime.now)
    source    = IntegerField(null=False)
    types     = IntegerField(null=False)
    msg       = TextField(null=False)
