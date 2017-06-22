#!flask/bin/python

from flask import Flask, jsonify, request, abort, make_response, url_for
from flask_httpauth import HTTPBasicAuth

import requests, json

auth = HTTPBasicAuth()
app = Flask(__name__)

@auth.get_password
def get_password(username):
	if username == 'admin':
		return 'flask'
	return None

@auth.error_handler
def unauthorized():
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

@app.route('/rackhd/login', methods=['POST'])
@auth.login_required
def rackhd_login():
	if not request.json or not 'username' in request.json:
		abort(400)

	username = request.json['username']
	password = request.json['password']

	url = "https://localhost:8443/login"

	headers = {
		"Content-Type": "application/json"
	}

	payload = '{"username": "' + username + '", "password": "' + password + '"}'

	response = requests.post(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/skus/create', methods=['PUT'])
@auth.login_required
def create_skus():
	url = "https://localhost:8443/api/current/skus"

	token = request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	name = request.json['name']
	path = request.json['path']
	contains = request.json['contains']
        path2 = request.json['path2']
	equals = request.json['equals']
	discoveryGraphName = request.json['discoveryGraphName']
	username = request.json['username']
	password = request.json['password']
	hostname = request.json['hostname']

	payload = '{"name": "' + name + '", "rules": [{	"path":"' + path + '", "contains":"' + contains + '"}, {"path":"' + path2 + '", "equals":"' + equals + '"}], "discoveryGraphName": "' + discoveryGraphName + '", "discoveryGraphOptions":{"username": "' + username + '", "password": "' + password + '", "hostname": "' + hostname + '"}}'

	response = requests.put(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/skus/read', methods=['GET'])
@auth.login_required
def read_skus():
	url = "https://localhost:8443/api/current/skus"

	Token = request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": Token
	}

	response = requests.get(url, headers=headers, verify=False)

	return response.text

@app.route('/rackhd/skus/update', methods=['PATCH'])
@auth.login_required
def update_skus():
	base_url = "https://localhost:8443/api/current/skus"

	id = request.json['id']

	url = base_url + "/" + id

	token = request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	field = request.json['field']
	data = request.json['data']

	payload = '{"%s":"%s"}' % (field,data)

	response = requests.patch(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/skus/delete', methods=['DELETE'])
@auth.login_required
def delete_skus():
	base_url = "https://localhost:8443/api/current/skus"

	id = request.json['id']

	url = base_url + "/" + id

	token = request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

@app.route('/rackhd/nodes/create', methods=['POST'])
@auth.login_required
def create_nodes():

	url = "https://localhost:8443/api/current/nodes"

	Token = request.headers.get('Token')

	type = request.json['type']
	name = request.json['name']
#	service = request.json['service']

	headers = {
		"Content-Type":"application/json",
		"Authorization": Token
	}

	payload = '{"type":"' + type + '", "name":"' + name + '", "autoDiscover":false}'

	response = requests.post(url, headers=headers, data=payload, verify=False)
	return response.text

@app.route('/rackhd/nodes/read', methods=['GET'])
@auth.login_required
def read_nodes():
        url = "https://localhost:8443/api/current/nodes"

        Token = request.headers.get('Token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": Token
        }

        response = requests.get(url, headers=headers, verify=False)

        return response.text

@app.route('/rackhd/nodes/update', methods=['PATCH'])
@auth.login_required
def update_nodes():
	base_url = "https://localhost:8443/api/current/nodes"

	id = request.json['id']

	url = base_url + "/" + id

	token = request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	field = request.json['field']
	data = request.json['data']

	payload = '{"%s":"%s"}' % (field,data)

	response = requests.patch(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/nodes/delete', methods=['DELETE'])
@auth.login_required
def delete_nodes():
	base_url = "https://localhost:8443/api/current/nodes"

	id = request.json['id']

	url = base_url + "/" + id

	token = request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

if __name__ == '__main__':
	app.run(debug=True)
