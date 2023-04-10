import json
from bottle import get, post, delete, request, response
from models.Queue import Queue
from models.User import User
from models.Topic import Topic
from controllers.Middleware import has_body, body_req, auth, auth_query, enable_cors
from util.exceptions import DuplicatedUserException

@post('/User/new', apply=(has_body, body_req({'username', 'password'}), enable_cors))
def newUser():
    User.read()
    payload = json.load(request.body)
    username = payload['username']
    password = payload['password']

    try:
        User(username, password)

        User.write()
        return {'success': 1,
                'message': "Successfully created user"}
    except DuplicatedUserException:
        return {'success': 0,
                'message': 'Username already taken'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@get('/User/list', apply=(auth_query, enable_cors))
def listUsers():
    User.read()

    try:
        users = User.list()

        reply = []
        for user in users:
            reply.append({"username": user.name})
        return json.dumps(reply)
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@post('/User/delete', apply={has_body, body_req({'username', 'password'}), auth, enable_cors})
def deleteUser():
    User.read()
    Topic.read()
    payload = json.load(request.body)
    username = payload['username']

    user_id = User.attributesToId(username)

    try:
        topics = Topic.list()
        for topic in topics:
            topic.deleteSubscriber(user_id)

        user = User.users[user_id]
        user.delete()
        Topic.write()
        User.write()
        return {'success': 1,
                'message': 'Successfully deleted user'}
    except KeyError:
        return {'success': 0,
                'message': 'User not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}
