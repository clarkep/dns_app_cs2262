import socket
import time

# { domain_name: (ip, ttl, timestamp) }
dns_records = {}
error_response = "Invalid request"
not_found_response = "Not found"
success_response = "Success"

def dump_old_records():
    for name, record in dns_records.items():
        ip, ttl, timestamp = record
        if time.time() - timestamp > ttl:
            del dns_records[name]

# Returns: response as string
def generate_response(dnsrequest):
    print(dnsrequest)
    if "TYPE" not in dnsrequest or dnsrequest["TYPE"] != "A":
        return error_response    
    if "NAME" not in dnsrequest:
        return error_response
    # An update request:
    if "VALUE" in dnsrequest:
        if "TTL" not in dnsrequest:
            return error_response
        record = (dnsrequest["VALUE"], dnsrequest["TTL"], time.time())
        # write the record, possibly overwriting
        dns_records[dnsrequest["NAME"]] = record
        return success_response
    else:
        if dnsrequest["NAME"] in dns_records:
            name = dnsrequest["NAME"]
            ip, ttl, timestamp = dns_records[name]
            return "TYPE=A\nNAME={}\nVALUE={}\nTTL={}".format(name, ip, ttl)
        else:
            return not_found_response

def dns_server():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('0.0.0.0', 53533)
    server_socket.bind(server_address)

    print('DNS server is running on {}:{}'.format(*server_address))

    while True:
        # Receive DNS query from client
        data, client_address = server_socket.recvfrom(2048)
        # A nonstandard DNS request, sent as series of lines
        # of UTF-8 having the form KEY=VALUE.
        print("got request")
        lines = data.decode().split("\n")
        dnsrequest = {}
        for line in lines:
            if line:
                key, value = line.split("=")
                dnsrequest[key] = value
        response = generate_response(dnsrequest).encode()
        print("response: ", response)

        # Send the DNS response back to the client
        server_socket.sendto(response, client_address)
        print('Sent DNS response to {}:{}'.format(*client_address))

if __name__ == '__main__':
    dns_server()