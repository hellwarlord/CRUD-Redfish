#!flask/bin/python

from flask import Flask, jsonify, request, abort
from flask import make_response
import requests

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'admin123'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


app = Flask(__name__)

@app.route('/rackhd/login', methods=['POST'])
@auth.login_required
def login():

        user_name = request.json["username"]
        user_password = request.json["password"]
        user_role = request.json["role"]


        url = "https://localhost:8443/login"

        payload = '{ "username":"%s", "password":"%s", "role":"%s" }' % (user_name, user_password, user_role)

        headers= {

                "Content-Type": "application/json",

        }

        r = requests.post(url, headers=headers, data=payload, verify=False)
        return  r.text

if __name__ == '__main__':
        app.run(debug=True)
