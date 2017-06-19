#!flask/bin/python

from flask import Flask, jsonify, request, abort

import requests, json

app = Flask(__name__)

@app.route('/rackhd/login', methods=['POST'])
#@auth.login_required
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

@app.route('/rackhd/tags/create', methods=['PUT'])

def create_tags():
	url = "https://localhost:8443/api/current/tags"

	token = request.headers.get('Authorization')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	name = request.json['name']
	rules = request.json['rules']
	
	payload = '{"name": "' + name + '", "rules":"' + rule + '"}'

	response = requests.put(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/tags/read', methods=['GET'])

def read_tags():
	url = "https://localhost:8443/api/current/tags"

	token = request.headers.get('Authorization')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.get(url, headers=headers, verify=False)

	return response.text

@app.route('/rackhd/obms/update', methods=['GET'])

def update_tags():
	base_url = "https://localhost:8443/api/current/tags"

	name = request.json['name']

	url = base_url + "/:" + name

	token = request.headers.get('Authorization')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	name = request.json['name']
	rules = request.json['rules']
	
	payload = '{"name":"' + name +'", "rules":"' + rules + '"}}'

	response = requests.patch(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/tags/delete', methods=['DELETE'])

def delete_tags():
	base_url = "https://localhost:8443/api/current/tags"

	name = request.json['name']

	url = base_url + "/:" + name

	token = request.headers.get('Authorization')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

if __name__ == '__main__':
	app.run(debug=True)
