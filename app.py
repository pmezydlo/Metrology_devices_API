from flask import render_template, request
from flask import Flask
import json
from psql_interface import psql_connection

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

name = "measure_device_base"
user = "postgres"
password = "postgres"
host = "localhost"
base = 0

def add_devices(data): 
    own_name = data['own_name']
    lan_ip = data['lan_address']
    lan_port = data['lan_port']
    print('{} {} {}'.format(own_name, lan_ip, lan_port))

@app.route('/api/dev', methods=['POST', 'GET'])
def add_device():
    if request.method == 'POST':
        add_devices(json.loads(request.data))     
        
        #dev_data = base.get_device_json()
        #print dev_data
    return json.dumps(request.json)


@app.route("/")
def index():
    return render_template("index.html")
	
if __name__ == "__main__":
#    base = psql_connection(name, user, password, host)
    app.run()
