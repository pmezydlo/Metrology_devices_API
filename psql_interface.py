import sys
import time
import os
import psycopg2
import psycopg2.extras
import json
import datetime

class psql_connection(object):
    def __init__ (self, database, user, host, password):
        self.connect = None 
        self.database = database
        self.user = user
        self.host = host
        self.password = password
        try:
            self.database = database
            self.user = user
            self.connect = psycopg2.connect(database=self.database, user=self.user, host=self.host, password=self.password)     
        except psycopg2.DatabaseError, e:
            print('Database error {}'.format(e));
            sys.exit(1)

    def psql_disconnect(self):
        self.connect.close()

    def push_log_msg(self, msg, type):
        try:
            cur = self.connect.cursor()
            dt = datetime.datetime.now()
            d = dt.strftime("%d.%m.%y")
            t = dt.strftime("%H:%M:%S")
            cur.execute("INSERT INTO logs  VALUES (default, %s, %s, %s, %s)", (d, t, type, msg))
            self.connect.commit()
            cur.close()
        except:
            print "database error logs insert"

    def get_logs_json(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT  * FROM logs")      
            ret = cur.fetchall()
            cur.close()
            return json.dumps(ret)
        except:
            print "database logs error select"

    def del_logs(self):
        try:
            cur = self.connect.cursor()
            cur.execute("DELETE FROM logs")
            self.connect.commit()
            cur.close()   
        except:
            print "delete logs"

    def get_devices_list_json(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT  * FROM devices")      
            ret = cur.fetchall()
            cur.close()
            return json.dumps(ret) 
        except:
            print "database error select"

    def add_device_json(self, json_data):
        try:
            data = json.loads(json_data)
            cur = self.connect.cursor()
            cur.execute("INSERT INTO devices VALUES (default,  %s, '', '', '', '', %s, %s, 'NOREADY')", (data['own_name'], data['lan_address'], data['lan_port']))
            self.connect.commit()
            cur.close()
        except:
            print "database error insert"

    def del_device_by_id(self, dev_id):
        try:
            cur = self.connect.cursor()
            cur.execute("DELETE FROM devices WHERE id = %s", (dev_id,))
            self.connect.commit()
            cur.close()
        except:
            print "database error delete"

    def get_device_by_id(self, dev_id):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM devices WHERE id = %s", (dev_id,))
            ret = cur.fetchall()
            cur.close()
            return ret
        except:
            print "database error select"

    def get_tasks_list_json(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT  * FROM tasks")      
            ret = cur.fetchall()
            cur.close()
            return json.dumps(ret) 
        except:
            print "database error select"

    def add_task_json(self, json_data):
        try:
            data = json.loads(json_data)
            cur = self.connect.cursor()
            cur.execute("INSERT INTO tasks VALUES (default, %s, %s, %s, %s, default, %s, '')", (data['name'], data['dev'], data['date'], data['time'], data['msg'])) 
            self.connect.commit()
            cur.close()
        except:
            print "database error insert"

    def del_task_by_id(self, task_id):
        try:
            cur = self.connect.cursor()
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.connect.commit()
            cur.close()
        except:
            print "database error delete"

    def get_pending_task(self, d, t):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM tasks WHERE status = 'PENDING' AND date = %s AND time = %s", (d, t,))
            ret = cur.fetchall()
            cur.close()
            return ret
        except:
            print "database error select"

    def update_task_status(self, task_id, status):
        try:
            cur = self.connect.cursor()
            cur.execute("UPDATE tasks SET status=(%s) WHERE id = (%s)", (status, task_id,))
            self.connect.commit()
            cur.close()
        except:
            print "database error update staus"
