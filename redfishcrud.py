#!flask/bin/python
import urllib, requests
from flask import Flask, jsonify, request, json

app= Flask(__name__)

@app.route('/todo/api/v1.0/roles', methods=['GET'])
def get_role():

	url = "https://localhost:8443/api/current/roles"

	headers = {"Content-Type": "application/json", "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc0MzI0OTMsImV4cCI6MTQ5NzUxODg5M30.NpCbb-piLMUwln0j92wPyMUMxo4VLgbY7hkWy25gqSw"}

	request = requests.get(url, headers=headers, verify=False)

	return request.text

@app.route('/todo/api/v1.0/roles/post', methods=['POST'])
def post_role():

	role = request.json['role']
	privileges = request.json['privileges']

	privileges2 = list()

	for permission in privileges:
		privileges2.append(str(permission))

	privileges2 = str(privileges2)
	privileges2 = privileges2.replace("'",'"')

	url = "https://localhost:8443/api/current/roles"

	headers = {"Content-Type": "application/json", "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc0MzI0OTMsImV4cCI6MTQ5NzUxODg5M30.NpCbb-piLMUwln0j92wPyMUMxo4VLgbY7hkWy25gqSw"}

	payload = '{"privileges": ' + privileges2 + ', "role": "' + role + '"}'

	response = requests.post(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/todo/api/v1.0/roles/patch', methods=['PATCH'])
def patch_role():

	base_url = "https://localhost:8443/api/current/roles"

	role = request.json['role']

	privileges = request.json['privileges']

	privileges2 = list()

	for permission in privileges:
		privileges2.append(str(permission))

	privileges2 = str(privileges2)
	privileges2 = privileges2.replace("'",'"')

	url = base_url + "/" + role

	headers = {"Content-Type": "application/json", "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc0MzI0OTMsImV4cCI6MTQ5NzUxODg5M30.NpCbb-piLMUwln0j92wPyMUMxo4VLgbY7hkWy25gqSw"}

	payload = '{"privileges": ' + privileges2 + '}'

	response = requests.patch(url, headers=headers, data=payload,  verify=False)

	return response.text

@app.route('/todo/api/v1.0/roles/delete', methods=['DELETE'])

def delete_role():

	base_url = "https://localhost:8443/api/current/roles"

	role = request.json['role']

	url = base_url + "/" + role

	headers = {"Content-Type": "application/json", "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc0MzI0OTMsImV4cCI6MTQ5NzUxODg5M30.NpCbb-piLMUwln0j92wPyMUMxo4VLgbY7hkWy25gqSw"}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

@app.route('/todo/api/v1.0/ibms', methods=['GET'])
def get_ibm():
	url = "https://localhost:8443/api/current/ibms"

	headers = { "Content-Type": "application/json", "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc0MzI0OTMsImV4cCI6MTQ5NzUxODg5M30.NpCbb-piLMUwln0j92wPyMUMxo4VLgbY7hkWy25gqSw"}

	response = requests.get(url, headers=headers, verify=False)

	return response.text

@app.route('/todo/api/v1.0/ibms/post', methods=['PUT'])

def create_ibms():
	url = "https://localhost:8443/api/current/ibms"

	headers = {"Content-Type": "application/json", "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc0MzI0OTMsImV4cCI6MTQ5NzUxODg5M30.NpCbb-piLMUwln0j92wPyMUMxo4VLgbY7hkWy25gqSw"}

	nodeId = request.json['nodeId']
	service = request.json['service']
	community = request.json['community']
	host = request.json['host']

	payload = '{"nodeId": "' + nodeId + '", "service":"' + service + '", "config":{"community":"' + community + '", "host":"' + host + '"}}'

	response = requests.put(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/todo/api/v1.0/ibms/patch', methods=['PATCH'])

def patch_ibms():
	base_url = "https://localhost:8443/api/current/ibms"

	headers = {"Content-Type": "application/json", "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc0MzI0OTMsImV4cCI6MTQ5NzUxODg5M30.NpCbb-piLMUwln0j92wPyMUMxo4VLgbY7hkWy25gqSw"}

	nodeId = request.json['nodeId']

	url = base_url + "/" + nodeId

	service = request.json['service']
	community = request.json['community']
	host = request.json['host']

	payload = '{"nodeId": "' + nodeId + '", "service":"' + service + '", "config":{"community":"' + community + '", "host":"' + host + '"}}'

	response = requests.patch(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/todo/api/v1.0/ibms/delete', methods=['DELETE'])

def delete_ibms():
	base_url = "https://localhost:8443/api/current/ibms"

	nodeId = request.json['nodeId']

	headers = {"Content-Type": "application/json", "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc0MzI0OTMsImV4cCI6MTQ5NzUxODg5M30.NpCbb-piLMUwln0j92wPyMUMxo4VLgbY7hkWy25gqSw"}

	url = base_url + "/" + nodeId

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

if __name__ == '__main__':
	app.run(debug=True)
