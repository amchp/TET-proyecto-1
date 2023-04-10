import json
from bottle import request, response
from models.User import User

def has_body(f):
    def inner(*args, **kwargs):
        if request.json:
            return f(*args, **kwargs)
        response.status = 400
        return {'error': 'ValidationError',
                'error_message': 'Body is required (and must be JSON).'}
    return inner

def body_req(required):
    def body_req_middleware(f):
        def inner(*args, **kwargs):
            intersection = required.intersection(set(request.json.keys()))
            if intersection != required:
                response.status = 400
                return {'error': 'ValidationError',
                        'error_message': 'Key(s): {} are not in JSON payload'
                        ''.format(', '.join('{!r}'.format(k)
                                            for k in required - intersection))}
            return f(*args, **kwargs)
        return inner
    return body_req_middleware

def auth(f):
    def inner(*args, **kwargs):
        User.read()
        payload = json.load(request.body)
        username = payload['username']
        password = payload['password']
        for user in User.list():
            if user.name == username:
                if user.password == password:
                    return f(*args, **kwargs)
                response.status = 401
                return {'error': 'Unauthorized',
                        'error_message': 'Wrong credentials'}
        response.status = 401
        return {'success': 0,
            'message': 'User not found'}
    return inner

def auth_query(f):
    def inner(*args, **kwargs):
        User.read()
        username = request.query['username']
        password = request.query['password']
        for user in User.list():
            if user.name == username:
                if user.password == password:
                    return f(*args, **kwargs)
                response.status = 401
                return {'error': 'Unauthorized',
                        'error_message': 'Wrong credentials'}
        response.status = 401
        return {'success': 0,
                'message': 'User not found'}
    return inner

def enable_cors(f):
    def inner(*args, **kwargs):
        response.set_header('Access-Control-Allow-Origin', '*')
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        return f(*args, **kwargs)
    return inner
