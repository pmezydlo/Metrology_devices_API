from flask import render_template, request
from flask import Flask
import json
from psql_interface import psql_connection

app = Flask(__name__)
app.config['DEBUG'] = True

name = "measure_device_base"
user = "pmezydlo"
host = "localhost"
password = "pass"

@app.route('/api/dev', methods=['POST', 'GET'])
def add_device():
    if request.method == 'POST':
        base.add_device_json(request.data)
        print "ok"           
    return base.get_devices_list_json()

@app.route("/")
def index():
    return render_template("index.html")
	
if __name__ == "__main__":
    base = psql_connection(name, user, host, password)
    app.run()
