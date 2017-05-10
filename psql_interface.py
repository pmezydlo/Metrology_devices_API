import sys
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

    def push_log_msg(self, part_of_sys, type, msg):
        try:
            cur = self.connect.cursor()
            dt = datetime.datetime.now()
            d = dt.strftime("%d.%m.%y")
            t = dt.strftime("%H:%M:%S")
            cur.execute("INSERT INTO logs VALUES (default, %s, %s, %s, %s, %s)", (d, t, part_of_sys, type, msg,))
            self.connect.commit()
            cur.close()
        except psycopg2.Error as e:
            print("Logs {},{}".format(e.diag.severity, e.diag.message_primary))

    def get_logs_json(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT  * FROM logs")      
            ret = cur.fetchall()
            cur.close()
            return json.dumps(ret)
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def del_logs(self):
        try:
            cur = self.connect.cursor()
            cur.execute("DELETE FROM logs")
            self.connect.commit()
            cur.close()
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def get_devices_list_json(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT  * FROM devices")      
            ret = cur.fetchall()
            cur.close()
            return json.dumps(ret)
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def add_device_json(self, json_data):
        try:
            data = json.loads(json_data)
            cur = self.connect.cursor()
            cur.execute("INSERT INTO devices VALUES (default,  %s, %s, %s)", (data['own_name'], data['lan_address'], data['lan_port']))
            self.connect.commit()
            cur.close()
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def del_device_by_id(self, dev_id):
        try:
            cur = self.connect.cursor()
            cur.execute("DELETE FROM devices WHERE id = %s", (dev_id,))
            self.connect.commit()
            cur.close()
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def get_device_by_id(self, dev_id):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM devices WHERE id = %s", (dev_id,))
            ret = cur.fetchall()
            cur.close()
            return ret
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)


    def get_tasks_list_json(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT  * FROM tasks")      
            ret = cur.fetchall()
            cur.close()
            return json.dumps(ret)
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def add_task_json(self, json_data):
        try:
            data = json.loads(json_data)
            cur = self.connect.cursor()
            cur.execute("INSERT INTO tasks VALUES (default, %s, %s, %s, %s, default, %s, '')", (data['name'], data['dev'], data['date'], data['time'], data['msg'])) 
            self.connect.commit()
            cur.close()
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def del_task_by_id(self, task_id):
        try:
            cur = self.connect.cursor()
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.connect.commit()
            cur.close()
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def get_pending_task(self, d, t):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM tasks WHERE status = 'PENDING'") #AND date = %s AND time = %s", (d, t,))
            ret = cur.fetchall()
            cur.close()
            return ret
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def update_task_status(self, task_id, status):
        try:
            cur = self.connect.cursor()
            cur.execute("UPDATE tasks SET status=(%s) WHERE id = (%s)", (status, task_id,))
            self.connect.commit()
            cur.close()
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def get_task_request(self, task_id):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT (req) FROM tasks WHERE id = %s", (task_id,))
            ret = cur.fetchall()
            cur.close()
            return ret[0][0]
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)

    def push_task_request(self, task_id, msg):
        try:
            cur = self.connect.cursor()
            cur.execute("UPDATE tasks SET req=(%s) WHERE id = (%s)", (msg, task_id,))
            self.connect.commit()
            cur.close()
        except psycopg2.Error as e:
            self.push_log_msg('BASE', e.diag.severity, e.diag.message_primary)


