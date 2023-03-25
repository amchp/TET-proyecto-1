from models.Queue import Queue
from models.User import User


user1 = User(name='Alejandro Mc Ewen', password='password')
user2 = User(name='Elisa Rodriguez', password='password')
queues = {}
queue1 = Queue(user1.ID, user2.ID)
queue2 = Queue(user2.ID, user1.ID)
queue1.addMessage('HI')
queue1.addMessage('BYE')
queue2.addMessage('Cool')
queue2.addMessage('LOL')
queues[queue1.ID] = queue1
queues[queue2.ID] = queue2
