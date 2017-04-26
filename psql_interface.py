import sys
import time
import os
import psycopg2
import psycopg2.extras
import json

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
        finally:
            print "all is ok"

    def psql_disconnect(self):
        self.connect.close()

    def get_device_list(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM devices")
            cur.close()
            return cur.fetchall()

        except:
            print "database error select"

    def get_devices_list_json(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""SELECT  * FROM devices""")      
            
            return json.dumps(cur.fetchall()) 
        except:
            print "database error select"


    def add_device_json(self, json_data):
        try:
            data = json.loads(json_data)
            cur = self.connect.cursor()
            cur.execute("INSERT INTO devices(own_name, lan_address, lan_port) VALUES (%s, %s, %s)", (data['own_name'], data['lan_address'], data['lan_port']))
            self.connect.commit()
        except:
            print "database error insert"



