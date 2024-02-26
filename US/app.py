from flask import Flask
from flask import request
app = Flask(__name__)

import socket
import requests
import time
import os

def do_dns_lookup(hostname, as_ip, as_port):
    print('Sending DNS request to AS')
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send a DNS request to the AS
    message = 'TYPE=A\nNAME={}'.format(hostname)
    client_socket.sendto(message.encode(), (as_ip, int(as_port)))

    # Receive the DNS response from the AS
    data, server_address = client_socket.recvfrom(2048)
    client_socket.close()

    if data.decode() == 'Not found':
        print('DNS record not found')
        return None

    # Parse the DNS response
    lines = data.decode().split("\n")
    dnsresponse = {}
    for line in lines:
        if line:
            key, value = line.split("=")
            dnsresponse[key] = value

    if 'VALUE' not in dnsresponse:
        print('Malformed DNS response')
        return None

    return dnsresponse['VALUE']

def do_fs_request(fs_ip, fs_port, number):
    print('Sending request to FS')
    # Send a request to the FS
    url = 'http://{}:{}/fibonacci'.format(fs_ip, fs_port)
    params = {
        'number': number,
    }
    response = requests.get(url, params=params)
    print(f'Status Code: {response.status_code}')
    print(f'Response Body: {response.text}')
    if response.status_code != 200:
        print('Error: FS request failed')
        return None 
    else:
        return int(response.text)


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

    fs_ip = do_dns_lookup(hostname, as_ip, as_port)
    if fs_ip:
        n = do_fs_request(fs_ip, fs_port, number)
    
    if isinstance(n, int):
        return "Fibonacci number {} is {}.\n Have a nice day!".format(number, n)
    else:
        return "Error getting your fibonacci number", 400

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
