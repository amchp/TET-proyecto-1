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
    return inner