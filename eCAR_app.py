from flask import Flask, jsonify
import json
import ipaddress

app = Flask(__name__)

def load_data(): 
    data = []
    with open('data.json') as file:
        for line in file:
            json_object = json.loads(line)
            data.append(json_object)
    return data

def valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False

def valid_ipv6(ip):
    try:
        ipaddress.IPv6Address(ip)
        return True
    except ValueError:
        return False

@app.route('/1')
def get_unique_actions():
    action_count = {}
    data = load_data()

    for record in data:
        action = record.get('action')
        if action:
            action_count[action] = action_count.get(action, 0) + 1
    
    return jsonify({'unique_action_count': len(action_count)})

@app.route('/2')
def get_action_occurrences():
    action_count = {}
    data = load_data()

    for record in data:
        action = record.get('action')
        if action:
            action_count[action] = action_count.get(action, 0) + 1

    return jsonify({'action_occurances' : action_count})

@app.route('/3')
def get_ip_breakdown():
    ipv4_count = 0
    ipv6_count = 0
    invalid_ip_count = 0
    data = load_data()

    for record in data:
        properties = record.get('properties', {})
        src_ip = properties.get('src_ip')
        if valid_ipv4(src_ip):
            ipv4_count += 1
        elif valid_ipv6(src_ip):
            ipv6_count += 1
        else:
            invalid_ip_count += 1
    return jsonify({'IPv4_count': ipv4_count, 'IPv6_count': ipv6_count, 'invalid_or_missing_IP_count': invalid_ip_count})

@app.route('/4')
def get_subnet_count():
    subnet_count = 0
    data = load_data()

    for record in data:
        properties = record.get('properties', {})
        dest_ip = properties.get('dest_ip')
        if dest_ip and valid_ipv4(dest_ip):
            if ipaddress.IPv4Address(dest_ip) in ipaddress.IPv4Network('224.0.0.0/8'):
                subnet_count += 1

    return jsonify({'subnet_count': subnet_count})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)