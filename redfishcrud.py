#!flask/bin/python

import urllib, requests
from flask import Flask, jsonify, request, json
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app= Flask(__name__)

@auth.get_password
def get_password(username):
	if username == 'admin':
		return 'admin123'
	return None

@auth.error_handler
def unauthorizaed():
	return make_response(jsonify({'error': 'Flask unauthorized access'}), 401)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error':'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
	return make_response(jsonify({'error':'Method not allowed'}), 405)

@app.route('/todo/api/v1.0/roles/get', methods=['GET'])
@auth.login_required
def get_role():

	url = "https://localhost:8443/api/current/roles"

	token = "JWT " + request.headers.get('Token')

	headers = {"Content-Type": "application/json", "Authorization": token }

	response = requests.get(url, headers=headers, verify=False)

	return response.text

@app.route('/todo/api/v1.0/roles/post', methods=['POST'])
@auth.login_required
def post_role():

	role = request.json['role']
	privileges = request.json['privileges']

	privileges2 = list()

	for permission in privileges:
		privileges2.append(str(permission))

	privileges2 = str(privileges2)
	privileges2 = privileges2.replace("'",'"')

	url = "https://localhost:8443/api/current/roles"

	token = "JWT " + request.headers.get('Token')

	headers = {"Content-Type": "application/json", "Authorization": token }

	payload = '{"privileges": ' + privileges2 + ', "role": "' + role + '"}'

	response = requests.post(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/todo/api/v1.0/roles/patch', methods=['PATCH'])
@auth.login_required
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

	token = "JWT " + request.headers.get('Token')

	headers = {"Content-Type": "application/json", "Authorization": token }

	payload = '{"privileges": ' + privileges2 + '}'

	response = requests.patch(url, headers=headers, data=payload,  verify=False)

	return response.text

@app.route('/todo/api/v1.0/roles/delete', methods=['DELETE'])
@auth.login_required
def delete_role():

	base_url = "https://localhost:8443/api/current/roles"

	role = request.json['role']

	url = base_url + "/" + role

	token = "JWT " + request.headers.get('Token')

	headers = {"Content-Type": "application/json", "Authorization": token }

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

@app.route('/todo/api/v1.0/ibms/get', methods=['GET'])
@auth.login_required
def get_ibm():

	url = "https://localhost:8443/api/current/ibms"

	token = "JWT " + request.headers.get('Token')

	headers = {"Content-Type": "application/json", "Authorization": token }

	response = requests.get(url, headers=headers, verify=False)

	return response.text

@app.route('/todo/api/v1.0/ibms/post', methods=['PUT'])
@auth.login_required
def create_ibms():

	url = "https://localhost:8443/api/current/ibms"

	token = "JWT " + request.headers.get('Token')

	headers = {"Content-Type": "application/json", "Authorization": token }

	nodeId = request.json['nodeId']
	service = request.json['service']
	community = request.json['community']
	host = request.json['host']

	payload = '{"nodeId": "' + nodeId + '", "service":"' + service + '", "config":{"community":"' + community + '", "host":"' + host + '"}}'

	response = requests.put(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/todo/api/v1.0/ibms/patch', methods=['PATCH'])
@auth.login_required
def patch_ibms():

	base_url = "https://localhost:8443/api/current/ibms"

	token = "JWT " + request.headers.get('Token')

	headers = {"Content-Type": "application/json", "Authorization": token }

	nodeId = request.json['nodeId']

	url = base_url + "/" + nodeId

	service = request.json['service']
	community = request.json['community']
	host = request.json['host']

	payload = '{"nodeId": "' + nodeId + '", "service":"' + service + '", "config":{"community":"' + community + '", "host":"' + host + '"}}'

	response = requests.patch(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/todo/api/v1.0/ibms/delete', methods=['DELETE'])
@auth.login_required
def delete_ibms():

	base_url = "https://localhost:8443/api/current/ibms"

	nodeId = request.json['nodeId']

	token = "JWT " + request.headers.get('Token')

	headers = {"Content-Type": "application/json", "Authorization": token }

	url = base_url + "/" + nodeId

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

if __name__ == '__main__':
	app.run(debug=True)
