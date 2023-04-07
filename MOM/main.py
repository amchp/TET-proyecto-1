from controllers import QueueController, TopicController, UserController
from bottle import run
from config import PORT

if __name__ == '__main__':
    run(host='localhost', port=PORT)