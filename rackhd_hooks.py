#!flask/bin/python

from flask import Flask, jsonify, request, abort

import requests

app = Flask(__name__)

@app.route('/rackhd/hooks', methods=['GET'])
def readhook():

        token = request.headers.get('token')
        url = "https://localhost:8443/api/2.0/hooks"

        headers = {

                "Content-Type":"application/json",
                "Authorization":"JWT "+token
        }
        r = requests.get(url, headers=headers, verify=False)

        return r.text

@app.route('/rackhd/hooks/create', methods=['POST'])
def createuser():

        url_name = request.json["url"]

        token = request.headers.get('token')
        url = "https://localhost:8443/api/2.0/hooks"

        payload = '{ "url":"%s" }' % (url_name)

        headers= {

                "Content-Type": "application/json",
                "Authorization": "JWT "+token
        }

        r = requests.post(url, headers=headers, data=payload, verify=False)
        return  r.text

@app.route('/rackhd/hooks/update', methods=['PATCH'])
def patchuser():

        user_id  = request.json["id"]
        new_name = request.json["name"]

        token = request.headers.get('token')

        url = "https://localhost:8443/api/2.0/hooks/%s" % user_id

        headers= {

                "Content-Type":"application/json",
                "Authorization":"JWT "+token
        }

        payload = '{ "name": "%s" }' % new_name

        r = requests.patch(url, data=payload, headers=headers, verify=False)

        return r.text

@app.route('/rackhd/hooks/delete', methods=['DELETE'])
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
