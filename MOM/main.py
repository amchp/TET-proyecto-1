from controllers import QueueController, TopicController, UserController
from bottle import run

if __name__ == '__main__':
    run(host='localhost', port=8080)