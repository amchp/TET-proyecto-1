import json
from bottle import get, post, request, response
from models.Topic import Topic
from models.User import User
from models.Queue import Queue
from controllers.Middleware import has_body, body_req, auth, enable_cors

@post('/Topic/send', apply=(has_body, body_req({'username', 'password', 'topic', 'message'}), auth, enable_cors))
def sendToTopic():
    Topic.read()
    Queue.read()
    payload = json.load(request.body)
    username = payload['username']
    topic_name = payload['topic']
    message = payload['message']

    user_id = User.attributesToId(username)
    topic_id = Topic.attributesToId(topic_name)
    try:
        topic = Topic.topics[topic_id]

        topic.addMessage(user_id, message)
        Queue.write()
        return {'success': 1,
                'message': 'successfully added message to Topic'}
    except KeyError:
        return {'success': 0,
                'message': 'Topic not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@post('/Topic/subscribe', apply=(has_body, body_req({'username', 'password', 'topic'}), auth, enable_cors))
def subscribeToTopic():
    Topic.read()
    payload = json.load(request.body)
    username = payload['username']
    topic_name = payload['topic']

    user_id = User.attributesToId(username)
    topic_id = Topic.attributesToId(topic_name)
    try:
        topic = Topic.topics[topic_id]

        topic.addSubscriber(user_id)
        Topic.write()
        return {'success': 1,
                'message': 'Successfully subscribed to Topic'}
    except KeyError:
        return {'success': 0,
                'message': 'Topic not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@post('/Topic/unsubscribe', apply=(has_body, body_req({'username', 'password', 'topic'}), auth, enable_cors))
def unsubscribeFromTopic():
    response.set_header('Access-Control-Allow-Origin', '*')
    Topic.read()
    payload = json.load(request.body)
    username = payload['username']
    topic_name = payload['topic']

    user_id = User.attributesToId(username)
    topic_id = Topic.attributesToId(topic_name)
    try:
        topic = Topic.topics[topic_id]

        topic.deleteSubscriber(user_id)
        Topic.write()
        return {'success': 1,
                'message': 'Successfully unsubscribed from Topic'}
    except KeyError:
        return {'success': 0,
                'message': 'Topic not found'}
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}

@get('/Topic/list', apply=(enable_cors))
def listTopics():
    Topic.read()

    try:
        topics = Topic.list()

        reply = []
        for topic in topics:
          reply.append({'topicName': topic.name})
        return json.dumps(reply)
    except:
        response.status = 500
        return {'success': 0,
                'message': 'Something unexpected happened'}
