from flask import Flask
from flask import request
app = Flask(__name__)

import time
import os

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number  = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    return "You requested hostname = " + hostname + ", fs_port = " + fs_port\
        + ", number = " + number + ", as_ip = " + as_ip + ", as_port = " + as_port

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
