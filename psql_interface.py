import sys
import time
import os
import psycopg2
import psycopg2.extras

class psql_connection(object):
    def __init__ (self, database, user, password, host):
        self.connect = None 
        self.database = database
        self.user = user
        self.password = password
        self.host = host

        try:
            self.database = database
            self.user = user
            self.connect = psycopg2.connect(database=self.database, user=self.user, host=self.host, password=self.password)     
        except psycopg2.DatabaseError, e:
            print('Database error {}'.format(e));
            sys.exit(1)
        finally:
            print "all is ok"

    def psql_print(self, dev_name):
        print('data_base_request from thread: {} addres:{}'.format(dev_name, hex(id(object))))
   
    def psql_disconnect(self):
        self.connect.close()

    def get_device_list(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT  id, own_name, lan_address, lan_port FROM devices")
            
            return cur.fetchall()

        except:
            print "database error select"
            sys.exit(1)

    def get_device_json(self):
        try: 
            cur = self.connect.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("SELECT  id, own_name, lan_address, lan_port FROM devices")           
            r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
            return (r[0] if r else None) if one else r

        except:
            print "database error select"
            sys.exit(1)


