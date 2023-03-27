import json
from bottle import post, request, response
from models.Queue import Queue
from models.User import User
from controllers.Middleware import has_body, body_req, auth

@post('/Queue/send', apply=(has_body, body_req({'username', 'password', 'queue', 'message'}), auth))
def sendToQueue():
    User.read()
    Queue.read()
    payload = json.load(request.body)
    username = payload['username']
    queue = payload['queue']
    message = payload['message']

    users = User.list()
    for user in users:
        if user.name == username:
            queues = Queue.list()
            for q in queues:
                if q.ID == queue:
                    if q.creator_id != user.ID:
                        return {'success': 0,
                                'message': 'Queue is owned by another user'}
                    q.addMessage(message)
                    Queue.write()
                    return {'success': 1,
                            'message': 'successfully added message'}
            return {'success': 0,
                    'message': 'Queue not found'}
    return {'success': 0,
            'message': 'User not found'}