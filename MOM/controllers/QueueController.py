import json
from bottle import get, post, delete, request, response
from models.Queue import Queue
from models.User import User
from controllers.Middleware import has_body, body_req, auth, auth_query, enable_cors
from util.exceptions import DuplicatedQueueException, QueueIsNotEmptyException

@post('/Queue/send', apply=(has_body, body_req({'username', 'password', 'queue', 'message'}), auth, enable_cors))
def sendToQueue():
    Queue.read()
    payload = json.load(request.body)
    username = payload['username']
    queue_id = payload['queue']
    message = payload['message']

    user_id = User.attributesToId(username)
    try:
        queue = Queue.queues[queue_id]

        if queue.creator_id != user_id:
            return {'success': 0,
                    'message': 'Queue is owned by another user'}
        queue.addMessage(message)
        Queue.write()
        return {'success': 1,
                'message': 'successfully added message to Queue'}
    except KeyError:
        return {'success': 0,
                'message': 'Queue not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@post('/Queue/retrieve', apply=(has_body, body_req({'username', 'password'}), auth, enable_cors))
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
        for m, creator in messages:
            reply.append({'message': m, 'sender': creator})
        Queue.write()
        return json.dumps(reply)
    except KeyError:
        return {'success': 0,
                'message': 'User not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@post('/Queue/new', apply=(has_body, body_req({'username', 'password', 'receiver'}), auth, enable_cors))
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

@get('/Queue/list', apply=(auth_query, enable_cors))
def listQueues():
    User.read()
    Queue.read()
    username = request.query['username']

    user_id = User.attributesToId(username)

    try:
        queues = Queue.queues.values()
        producer_queue = []
        consumer_queue = []
        for q in queues:
            if q.creator_id == user_id:
                producer_queue.append({"Queue": q.ID, "Receptor": User.idToName(q.receptor_id)})
            if q.receptor_id == user_id:
                consumer_queue.append({"Queue": q.ID, "Sender": User.idToName(q.creator_id)})
        return json.dumps({"ProducerOf": producer_queue, "ConsumerOf": consumer_queue})
    except KeyError:
        return {'success': 0,
                'message': 'User not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}
    
@post('/Queue/delete', apply=(has_body, body_req({'username', 'password', 'queue'}), auth, enable_cors))
def deleteQueue():
    User.read()
    Queue.read()
    payload = json.load(request.body)
    username = payload['username']
    queue_id = payload['queue']

    user_id = User.attributesToId(username)
    try:
        queue = Queue.queues[queue_id]

        if queue.creator_id != user_id:
            return {'success': 0,
                    'message': 'Queue is owned by another user'}
        
        receiver = User.users[queue.receptor_id]
        receiver.deleteQueue(queue_id)
        queue.delete()
        Queue.write()
        User.write()
        return {'success': 1,
                'message': 'Successfully deleted queue'}
    except KeyError:
        return {'success': 0,
                'message': 'Queue not found'}
    except QueueIsNotEmptyException:
        return {'success': 0,
                'message': 'Queue isn''t empty!'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

