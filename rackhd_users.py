#!flask/bin/python

from flask import Flask, jsonify, request, abort

import requests

app = Flask(__name__)

@app.route('/rackhd/users', methods=['GET'])
def readuser():
        token = request.headers.get('token')
        url = "https://localhost:8443/api/current/users"
        headers = {
                "Content-Type":"application/json",
                "Authorization":"JWT "+token
        }
        r = requests.get(url, headers=headers, verify=False)

        return r.text

@app.route('/rackhd/users/create', methods=['POST'])
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

        r = requests.post(url, headers=headers, data=payload, verify=False)
        return  r.text

@app.route('/rackhd/users/update', methods=['PATCH'])
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

        r = requests.delete(url, headers=headers, verify=False)

        url = "https://localhost:8443/api/current/users"

	payload = '{ "username":"%s", "password":"%s", "role":"%s" }' % (user_name, user_password, user_role)

        r = requests.post(url, headers=headers, data=payload, verify=False)
        return r.text

@app.route('/rackhd/users/delete', methods=['DELETE'])
def deleteuser():
        user_name = request.json["username"]

        token = request.headers.get('token')

        url = "https://localhost:8443/api/current/users/%s" % user_name

        headers= {
        "Content-Type":"application/json",
        "Authorization":"JWT "+token
        }

        r = requests.delete(url, headers=headers, verify=False)
        return r.text

if __name__ == '__main__':
        app.run(debug=True)
