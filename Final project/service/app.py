from flask import Flask, jsonify, abort, make_response, request, Response
from database.connection import database_session, init_database, Manipulator

app = Flask(__name__)
manipulator = Manipulator()

# Errors

def check_errors(keys, request):
    error = []

    if not request:
        error.append('You should add a body in your request')
        return error

    for key in keys:
        if not key in request:
            error.append('The ' + key + ' cannot be undefined')

    return error

@app.errorhandler(404) # Not found error.
def not_found(error):
    return make_response(jsonify({ 'error': 'Not found' }), 404)

@app.errorhandler(400) # Bad request from the user.
def bad_request(error):
    return make_response(jsonify({ 'error': 'Bad request' }), 400)

# User requests

@app.route('/users', methods = ['GET', 'POST', 'DELETE'])
def api_users():
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_users_id() })

    elif request.method == 'POST':
        error = check_errors(['username', 'user_id', 'email', 'name'], \
        request.json)

        if error:
            return make_response(jsonify({ 'error': error }), 400)

        if manipulator.get_users_id([request.json['user_id']]) or \
        manipulator.get_users_username([request.json['username']]):
            error.append('Such user exists already')
            return make_response(jsonify({ 'error': error }), 400)

        user = {
            'username' : request.json['username'],
            'user_id': request.json['user_id'],
            'email': request.json['email'],
            'name': request.json['name']
        }

        manipulator.save_user(user['username'], user['user_id'], \
            user['email'], user['name'])

        return jsonify({ 'user': [user] }), 201

    elif request.method == 'DELETE':
        manipulator.delete_users()
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

@app.route('/users/<int:user_id>', methods = ['GET', 'PATCH', 'PUT', 'DELETE'])
def api_user(user_id):
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_users_id([user_id]) })

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

    else:
        abort(404)

# Sensor requests

@app.route('/sensors', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_sensors():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

    else:
        abort(404)

@app.route('/sensors/<int:sensor_id>', methods = ['GET', 'POST', 'PATCH', \
    'PUT', 'DELETE'])
def api_sensor(sensor_id):
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

    else:
        abort(404)

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
