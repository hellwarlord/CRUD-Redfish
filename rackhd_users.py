#!flask/bin/python

from flask import Flask, jsonify, request, abort, make_response
import requests,json


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

if __name__ == '__main__':
        app.run(debug=True)
