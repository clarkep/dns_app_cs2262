import requests

url = 'http://localhost:9090/register'

data =  {
    "hostname": "fibonacci.com",
    "ip": "172.18.0.3",
    "as_ip": "172.18.0.4",
    "as_port": "53533",
}

# Not sure this is necessary
headers = {
    'Content-Type': 'application/json',
}

response = requests.put(url, json=data, headers=headers)

print(f'Status Code: {response.status_code}')
print(f'Response Body: {response.text}')
