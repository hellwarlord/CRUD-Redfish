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
