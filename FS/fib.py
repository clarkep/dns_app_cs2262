from flask import Flask, request
import socket

app = Flask(__name__)

default_ttl = 10000
as_success_response = "Success"

# Received a register PUT, so contact the AS over UDP to register our domain
# Returns: the AS's response as a string
def handle_register_request(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    message = "TYPE=A\nNAME={}\nVALUE={}\nTTL={}".format(
            data["hostname"], data["ip"], default_ttl)
    client_socket.sendto(message.encode(), 
            (data["as_ip"], int(data["as_port"])))
    
    response, server_address = client_socket.recvfrom(2048)
    client_socket.close()
    return response.decode()


@app.route('/')
def hello_world():
    return 'You have reached FS!'

@app.route('/register', methods=['PUT'])
def register():
    # Get the data from the request
    data = request.get_json()
    print("FS: got register request")
    as_response = handle_register_request(data)

    if as_response==as_success_response:
        return as_response, 201
    else:
        return as_response, 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=9090,
            debug=True)