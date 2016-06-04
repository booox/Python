# Python web service.

from flask import Flask, jsonify, abort, make_response, request, Response
from database.connection import Manipulator

app = Flask(__name__)
manipulator = Manipulator() # Create an instance of Manipulator.

# Errors

 # check_errors is a function to check an object and its keys to see if they
 # are empty.
def check_errors(keys, request):
    error = []

    if not request: # There is no point to continue here, early return.
        error.append('You should add a body in your request')
        return error

    for key in keys: # Iterate for every key and check if it is there.
        if not key in request:
            error.append('The ' + key + ' cannot be undefined')

    return error

# Errors are sent as an array with the key 'error' for consistency even
# if there is only one error.

# Data is sent as an array with the key 'data' for consistency even if
# there is only one object or one type.

# Messages are sent as an array with the key 'message' for consistency even
# if there is only one message.

# The clients will be happy about this.

# Both requests that target to one of the user or sensor take the id as a
# parameter, not the user_id nor the sensor_id for obvious reasons. When saving
# an id to the database in a client, I'd prefer as a client developer to
# be just a simple int and not a hash from an address, etc.

@app.errorhandler(404) # Not found error.
def not_found(error):
    return make_response(jsonify({ 'error': ['Not found'] }), 404)

@app.errorhandler(400) # Bad request from the user.
def bad_request(error):
    return make_response(jsonify({ 'error': ['Bad request'] }), 400)

# User requests

# The /users endpoint can GET and POST, in this case also can DELETE
# to just delete all the users in the database. It cannot PATCH or PUT for
# obvious reasons (what to patch.)

@app.route('/users', methods = ['GET', 'POST', 'DELETE'])
def api_users():
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_users_id() })

    elif request.method == 'POST':
        error = check_errors(['username', 'user_id'], request.json)

        if error: # This error is if the body is invalid.
            return make_response(jsonify({ 'error': error }), 400)

        # If the user_id or the username are already taken, error.
        if manipulator.get_users_id([request.json['user_id']]) or \
        manipulator.get_users_username([request.json['username']]):
            error.append('Such user exists already')
            return make_response(jsonify({ 'error': error }), 400)

        # Creates the user object with the initial values and the username
        # and user_id.
        user = {
            'username' : request.json['username'],
            'user_id': request.json['user_id'],
            'name': None,
            'email': None,
            'mean_temperature': None
        }

        if 'name' in request.json:
            user['name'] = request.json['name']

        if 'email' in request.json:
            user['email'] = request.json['email']

        if 'mean_temperature' in request.json:
            user['mean_temperature'] = request.json['mean_temperature']

        # Save and return with a 201.
        manipulator.save_user(user['username'], user['user_id'], \
            user['name'], user['email'], user['mean_temperature'])

        return jsonify({ 'data': [user] }), 201

    elif request.method == 'DELETE':
        manipulator.delete_users()
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

# In this case you cannot POST since the id is autogenerated.
@app.route('/users/<int:id>', methods = ['GET', 'PATCH', 'PUT', 'DELETE'])
def api_user(id):
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_users_id([id]) })

    elif request.method == 'PATCH':
        # Patch changes whatever is in the body, that means that it needs to be
        # checked what to change.

        user = manipulator.get_user(id)

        if not user:
            return make_response(jsonify({ 'error': ['No such user'] }), 400)

        # If there is a username we check if such username is taken,
        # same thing with the user_id.
        if 'username' in request.json:
            if manipulator.get_users_username([request.json['username']]) \
            and user.username != request.json['username']:
                return make_response(jsonify({ 'error': \
                ['Such user exists already'] }), 400)

            user.username = request.json['username']

        if 'user_id' in request.json:
            if manipulator.get_users_user_id([request.json['user_id']]) \
            and str(user.user_id) != str(request.json['user_id']):
                return make_response(jsonify({ 'error': \
                ['Such user exists already'] }), 400)

            user.user_id = request.json['user_id']

        if 'email' in request.json:
            user.email = request.json['email']

        if 'name' in request.json:
            user.name = request.json['name']

        if 'mean_temperature' in request.json:
            user.mean_temperature = request.json['mean_temperature']

        manipulator.commit()

        # user.serialize() returns an object from a user.
        return jsonify({ 'message': [user.serialize()] }), 200

    elif request.method == 'PUT':
        # PUT basically puts None if the value is not defined in the request,
        # that means that the username and the user_id need to be defined in
        # the body.

        error = check_errors(['user_id', 'username'], request.json)

        if error:
            return make_response(jsonify({ 'error': error }), 400)

        # We get the user that we're gonna manipulate.
        user = manipulator.get_user(id)

        if not user:
            return make_response(jsonify({ 'error': ['No such user'] }), 400)

        # Same thing that we did in the patch, if the username exists in the db
        # and it's not ours, this is an error, if it exists but it's ours,
        # everything is good, we can change it.

        if manipulator.get_users_username([request.json['username']]) \
        and user.username != request.json['username']:
            return make_response(jsonify({ 'error': \
            ['Such user exists already'] }), 400)

        user.username = request.json['username']

        if manipulator.get_users_user_id([request.json['user_id']]) \
        and str(user.user_id) != str(request.json['user_id']):
            return make_response(jsonify({ 'error': \
            ['Such user exists already'] }), 400)

        user.user_id = request.json['user_id']

        # Short if notation to check if it exists, if not, we'll set None.
        user.email = request.json['email'] if 'email' in request.json else None
        user.name = request.json['name'] if 'name' in request.json else None
        user.mean_temperature = request.json['mean_temperature'] \
        if 'mean_temperature' in request.json else None

        manipulator.commit()

        return jsonify({ 'message': [user.serialize()] }), 200

    elif request.method == 'DELETE':
        manipulator.delete_users(id)
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

# Sensor requests

# /sensors is basically the same as users, but changing the database from
# users to Temperatures.

@app.route('/sensors', methods = ['GET', 'POST', 'DELETE'])
def api_sensors():
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_temperatures_id() })

    elif request.method == 'POST':
        error = check_errors(['sensor_id'], request.json)

        if error:
            return make_response(jsonify({ 'error': error }), 400)

        if manipulator.get_temperatures_sensors([request.json['sensor_id']]):
            error.append('Such sensor exists already')
            return make_response(jsonify({ 'error': error }), 400)

        # Object with default values to edit later.
        sensor = {
            'sensor_id' : request.json['sensor_id'],
            'mean_temperature': None
        }

        if 'mean_temperature' in request.json:
            sensor['mean_temperature'] = request.json['mean_temperature']

        # Save the object we created to the database.
        manipulator.save_temperature(sensor['sensor_id'], \
        sensor['mean_temperature'])

        return jsonify({ 'data': [sensor] }), 201

    elif request.method == 'DELETE':
        manipulator.delete_temperatures()
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

@app.route('/sensors/<int:id>', methods = ['GET', 'PATCH', 'PUT', 'DELETE'])
def api_sensor(id):
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_temperatures_id([id]) })

    elif request.method == 'PATCH':
        sensor = manipulator.get_temperature(id)

        if not sensor:
            return make_response(jsonify({ 'error': ['No such sensor'] }), 400)

        if 'sensor_id' in request.json:
            if manipulator.get_temperatures_sensors([request.json['sensor_id']]) \
            and str(sensor.sensor_id) != str(request.json['sensor_id']):
                return make_response(jsonify({ 'error': \
                ['Such sensor exists already'] }), 400)

            sensor.sensor_id = request.json['sensor_id']

        if 'mean_temperature' in request.json:
            sensor.mean_temperature = request.json['mean_temperature']

        manipulator.commit()

        return jsonify({ 'message': [sensor.serialize()] }), 200

    elif request.method == 'PUT':
        if not 'sensor_id' in request.json:
            return make_response(jsonify({ 'error': \
            ['The sensor_id cannot be undefined'] }), 400)

        sensor = manipulator.get_temperature(id)

        if not sensor:
            return make_response(jsonify({ 'error': ['No such user'] }), 400)

        if manipulator.get_temperatures_sensors([request.json['sensor_id']]) \
        and str(sensor.sensor_id) != str(request.json['sensor_id']):
            return make_response(jsonify({ 'error': \
            ['Such sensor exists already'] }), 400)

        # No need to check if the sensor exists because it has been checked
        # already.
        sensor.sensor_id = request.json['sensor_id']
        sensor.mean_temperature = request.json['mean_temperature'] if \
        'mean_temperature' in request.json else None

        manipulator.commit()

        return jsonify({ 'message': [sensor.serialize()] }), 200

    elif request.method == 'DELETE':
        manipulator.delete_temperatures(id)
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

if __name__ == '__main__':
    # Initialize the manipulator and run the app in debug mode.
    manipulator.initialize()
    app.run(debug=True)
