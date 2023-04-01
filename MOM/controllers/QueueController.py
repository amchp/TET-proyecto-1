import json
from bottle import get, post, request, response
from models.Queue import Queue
from models.User import User
from controllers.Middleware import has_body, body_req, auth
from exceptions.exceptions import DuplicatedQueueException

@post('/Queue/send', apply=(has_body, body_req({'username', 'password', 'queue', 'message'}), auth))
def sendToQueue():
    Queue.read()
    payload = json.load(request.body)
    username = payload['username']
    queue = payload['queue']
    message = payload['message']

    user_id = User.attributesToId(username)
    try:
        q = Queue.queues[queue]

        if q.creator_id != user_id:
            return {'success': 0,
                    'message': 'Queue is owned by another user'}
        q.addMessage(message)
        Queue.write()
        return {'success': 1,
                'message': 'successfully added message to Queue'}
    except KeyError:
        return {'success': 0,
                'message': 'Topic not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@post('/Queue/retrieve', apply=(has_body, body_req({'username', 'password'}), auth))
def getMessages():
    User.read()
    Queue.read()
    payload = json.load(request.body)
    username = payload['username']
    
    user_id = User.attributesToId(username)
    try:
        user = User.users[user_id]

        messages = user.getMessages()
        reply = []
        for m in messages:
            reply.append({'message': m})
        Queue.write()
        return json.dumps(reply)
    except KeyError:
        return {'success': 0,
                'message': 'User not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@post('/Queue/new', apply=(has_body, body_req({'username', 'password', 'receiver'}), auth))
def newQueue():
    User.read()
    Queue.read()
    payload = json.load(request.body)
    username = payload['username']
    receiver = payload['receiver']

    user_id = User.attributesToId(username)
    receiver_id = User.attributesToId(receiver)

    try:
        Queue(user_id, receiver_id)

        queue_id = Queue.attributesToId(user_id, receiver_id)
        User.users[receiver_id].addQueue(queue_id)
        User.write()
        Queue.write()
        return {'success': 1,
                'message': "Successfully created queue"}
    except KeyError:
        return {'success': 0,
                'message': 'User not found'}
    except DuplicatedQueueException:
        return {'success': 0,
                'message': 'Queue already exists'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}