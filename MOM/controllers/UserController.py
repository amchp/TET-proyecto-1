import json
from bottle import get, post, delete, request, response
from models.Queue import Queue
from models.User import User
from models.Topic import Topic
from controllers.Middleware import has_body, body_req, auth, enable_cors
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

@get('/User/list', apply=(has_body, body_req({'username', 'password'}), auth, enable_cors))
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

@delete('/User/delete', apply={has_body, body_req({'username', 'password'}), auth, enable_cors})
def deleteUser():
    User.read()
    Queue.read()
    Topic.read()
    payload = json.load(request.body)
    username = payload['username']

    user_id = User.attributesToId(username)

    try:
        topics = Topic.list()
        for topic in topics:
            topic.deleteSubscriber(user_id)
        
        queues = Queue.list()
        delete_queue = []
        for queue in queues:
            if queue.creator_id == user_id:
                receiver_id = queue.receptor_id
                receiver = User.users[receiver_id]
                receiver.deleteQueue(queue.ID)
                for topic in topics:
                    if queue.ID in topic.queues.keys():
                        topic.deleteQueue(queue.ID)
                delete_queue.append(queue)
            elif queue.receptor_id == user_id:
                for topic in topics:
                    if queue.ID in topic.queues.keys():
                        topic.deleteQueue(queue.ID)
                delete_queue.append(queue)
        
        for queue in delete_queue:
            queue.delete()
        
        user = User.users[user_id]
        user.delete()
        Topic.write()
        Queue.write()
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