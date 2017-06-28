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

	data = '{"username": "' + username + '", "password": "' + password + '"}'
	res = requests.post(url, headers=headers, data=data, verify=False)
	return res.text

# OBMS (Lim Jin Tao Benjamin )
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
@auth.login_required
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
@auth.login_required
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
@auth.login_required
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

# roles (Lok Wei Yep)
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

# ibms (Lok Wei Yep)
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

# skus (Jubilian Ho Hong Yi)
@app.route('/rackhd/skus/create', methods=['PUT'])
@auth.login_required
def create_skus():
	url = "https://localhost:8443/api/current/skus"

	token = "JWT " + request.headers.get('Token')

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

	Token = "JWT " + request.headers.get('Token')

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

	token = "JWT " + request.headers.get('Token')

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

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

# nodes (Jubilian Ho Hong Yi)
@app.route('/rackhd/nodes/create', methods=['POST'])
@auth.login_required
def create_nodes():

	url = "https://localhost:8443/api/current/nodes"

	Token = "JWT " + request.headers.get('Token')

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

        Token = "JWT " + request.headers.get('Token')

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

	token = "JWT " + request.headers.get('Token')

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

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

# users (Wee Yu Xiang)
@app.route('/rackhd/users', methods=['GET'])
@auth.login_required
def readuser():
        token = request.headers.get('token')

	url = "https://localhost:8443/api/current/users"
        headers = {
                "Content-Type":"application/json",
                "Authorization":"JWT "+token
        }

	get_users = requests.get(url, headers=headers, verify=False)

        return get_users.text

@app.route('/rackhd/users/create', methods=['POST'])
@auth.login_required
def createuser():

        user_name = request.json["username"]
        user_password = request.json["password"]
        user_role = request.json["role"]

        token = request.headers.get('token')
        url = "https://localhost:8443/api/current/users"

        payload = '{ "username":"%s", "password":"%s", "role":"%s" }' % (user_name, user_password, user_role)

        headers= {

                "Content-Type": "application/json",
                "Authorization": "JWT "+token
        }

        post_user = requests.post(url, headers=headers, data=payload, verify=False)
        return  post_user.text

@app.route('/rackhd/users/update', methods=['PATCH'])
@auth.login_required
def patchuser():

        user_name = request.json["username"]
        user_password = request.json["password"]
        user_role = request.json["role"]

        token = request.headers.get('token')

        url = "https://localhost:8443/api/current/users/%s" % user_name

        headers= {
        "Content-Type":"application/json",
        "Authorization":"JWT "+token
        }

        delete_user = requests.delete(url, headers=headers, verify=False)

        url = "https://localhost:8443/api/current/users"

	payload = '{ "username":"%s", "password":"%s", "role":"%s" }' % (user_name, user_password, user_role)

        post_user = requests.post(url, headers=headers, data=payload, verify=False)
        return post_user.text

@app.route('/rackhd/users/delete', methods=['DELETE'])
@auth.login_required
def deleteuser():
        user_name = request.json["username"]

        token = request.headers.get('token')

        url = "https://localhost:8443/api/current/users/%s" % user_name

        headers= {
        "Content-Type":"application/json",
        "Authorization":"JWT "+token
        }

        delete_user = requests.delete(url, headers=headers, verify=False)
	return delete_user.text

# Hooks (Wee Yu Xiang)
@app.route('/rackhd/hooks', methods=['GET'])
@auth.login_required
def readhook():

        token = request.headers.get('token')
        url = "https://localhost:8443/api/2.0/hooks"

        headers = {

                "Content-Type":"application/json",
                "Authorization":"JWT "+token
        }
        get_hooks = requests.get(url, headers=headers, verify=False)

        return get_hooks.text

@app.route('/rackhd/hooks/create', methods=['POST'])
@auth.login_required
def createhook():

        url_name = request.json["url"]

        token = request.headers.get('token')
        url = "https://localhost:8443/api/2.0/hooks"

        payload = '{ "url":"%s" }' % (url_name)

        headers= {

                "Content-Type": "application/json",
                "Authorization": "JWT "+token
        }

        post_hook = requests.post(url, headers=headers, data=payload, verify=False)
        return  post_hook.text


@app.route('/rackhd/hooks/update', methods=['PATCH'])
@auth.login_required
def patchhook():

        user_id  = request.json["id"]
        new_name = request.json["name"]

        token = request.headers.get('token')

        url = "https://localhost:8443/api/2.0/hooks/%s" % user_id

        headers= {

                "Content-Type":"application/json",
                "Authorization":"JWT "+token
        }

        payload = '{ "name": "%s" }' % new_name

        patch_hook = requests.patch(url, data=payload, headers=headers, verify=False)

        return patch_hook.text

@app.route('/rackhd/hooks/delete', methods=['DELETE'])
@auth.login_required
def deletehook():
        user_id = request.json["id"]

        token = request.headers.get('token')

        url = "https://localhost:8443/api/2.0/hooks/%s" % user_id

        headers= {
        "Content-Type":"application/json",
        "Authorization":"JWT "+token
        }

        r = requests.delete(url, headers=headers, verify=False)
        return (r.text, r.status_code, r.headers.items())



if __name__ == '__main__':
	app.run(debug=True)

