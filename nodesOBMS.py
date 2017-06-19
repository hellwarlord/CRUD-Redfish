#!flask/bin/python

from flask import Flask, jsonify, request, abort, make_response

import requests, json

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

@auth.get_password
def get_password(username):
	if username == 'admin':
		return 'admin123'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# login for token
@app.route('/rackhd/login', methods=['POST'])
def rackhd_login():
	if not request.json or not 'username' in request.json:
		abort(400)

	username = request.json['username']
	password = request.json['password']


	url = "https://localhost:8443/login"

	headers = {
			"Content-Type": "application/json"
	}

	data = '{"username": "' + username + '", "password": "' + password + '"}'
	res = requests.post(url, headers=headers, data=data, verify=False)
	return res.text

# OBMS
@app.route('/rackhd/obms/read', methods=['GET'])
@auth.login_required
def readobms():
	url = "https://localhost:8443/api/current/obms"
	token = request.headers.get('token')

	headers = {
		"Content-Type" : "application/json",
		"Authorization":"JWT " + token

	}

	res = requests.get(url, headers=headers, verify=False)
	return res.text

@app.route('/rackhd/obms/create', methods=['PUT'])
def createobms():
	nodeId = request.json['nodeId']
	service = request.json['service']
	user = request.json['user']
	password = request.json['password']
	host = request.json['host']

	url = "https://localhost:8443/api/current/obms"
	token = request.headers.get('token')
	headers = {
		"Content-Type":"application/json",
		 "Authorization":"JWT " + token

	}

	data = '{"nodeId": "' + nodeId + '", "service":"' + service + '", "config":{"user":"' + user + '", "password":"' + password + '", "host":"' + host + '"}}'

	res = requests.put(url, headers=headers, data=data, verify=False)
	return res.text


@app.route('/rackhd/obms/update', methods=['PATCH'])
def updateobms():
	nodeId = request.json['nodeId']
	service = request.json['service']
	user = request.json['user']
	password = request.json['password']
	host = request.json['host']

	url = "https://localhost:8443/api/current/obms/" + nodeId
	token = request.headers.get('token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": "JWT " + token
	}


	data = '{"nodeId":"' + nodeId +'", "service":"' + service + '", "config":{"user":"' + user +'", "password":"' + password + '", "host":"' + host + '"}}'

	res = requests.patch(url, headers=headers, data=data, verify=False)
	return res.text


@app.route('/rackhd/obms/delete', methods=['DELETE'])
def deleteobms():
	nodeId = request.json['nodeId']
	url = "https://localhost:8443/api/current/obms/" + nodeId

	token = request.headers.get('token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": "JWT " + token
	}

	res = requests.delete(url, headers=headers, verify=False)

	return res.text

# Nodes
@app.route('/rackhd/nodes/read', methods=['GET'])
def readnodes():
	url = "https://localhost:8443/api/current/nodes"
	token = request.headers.get('token')
	headers = {
		"Content-Type":"application/json",
		"Authorization": "JWT " + token
	}

	res = requests.get(url, headers=headers, verify=False)
	return res.text

@app.route('/rackhd/nodes/create', methods=['POST'])
def createnodes():
	name = request.json['name']
	type = request.json['type']
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes"
	headers = {
		"Content-Type":"application/json",
		"Authorization": "JWT " + token
	}

	data = '{"name":"' + name + '", "type":"' + type + '", "autoDiscover":false}'

	res = requests.post(url, headers=headers, data=data, verify=False)
	return res.text

@app.route('/rackhd/nodes/update', methods=['PATCH'])
def updatenodes():
	id = request.json['id']
	name = request.json['name']
	type = request.json['type']
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes/" + id
	headers = {
		"Content-Type":"application/json",
		"Authorization":"JWT "+ token
	}

	data = '{"name":"' + name + '", "type":"' + type + '", "autoDiscover":false}'

	res = requests.patch(url, headers=headers, data=data, verify=False)
	return res.text

@app.route('/rackhd/nodes/delete', methods=['DELETE'])
def deletenodes():
	id = request.json['id']
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes/" + id

	headers = {
		"Content-Type":"application/json",
		"Authorization": "JWT " + token
	}

	res = requests.delete(url, headers=headers, verify=False)
	return res.text
# SKUs
@app.route('/rackhd/skus/read', methods=['GET'])
def readskus():
	url = "https://localhost:8443/api/current/skus"
	token = request.headers.get('token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": "JWT " + token
	}

	res = requests.get(url, headers=headers, verify=False)

	return res.text

@app.route('/rackhd/skus/create', methods=['PUT'])
def createskus():
	url = "https://localhost:8443/api/current/skus"
	token = request.headers.get('token')
	headers = {
		"Content-Type": "application/json",
		"Authorization": "JWT " + token
	}

	name = request.json['name']
	path = request.json['path']
	contains = request.json['contains']
	path = request.json['path']

	data = '{}'

	res = requests.put(url, headers=headers, data=data, verify=False)
	print res.text

@app.route('/rackhd/skus/delete', methods=['DELETE'])
def deleteskus():
	skuid = request.json['skuid']
	url = "https://localhost:8443/api/current/skus/" + skuid

	token = request.headers.get('token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": "JWT " + token
	}

	res = requests.delete(url, headers=headers, verify=False)


if __name__ == '__main__':
	app.run(debug=True)

