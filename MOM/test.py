from models.Topic import Topic
from models.Queue import Queue
from models.User import User


user1 = User(name='Alejandro Mc Ewen', password='password')
user2 = User(name='Elisa Rodriguez', password='password')

print(User.users)
User.write()
User.read()
print(User.users)


queue1 = Queue(user1.ID, user2.ID)
queue2 = Queue(user2.ID, user1.ID)
queue1.addMessage('HI')
queue1.addMessage('BYE')
queue2.addMessage('Cool')
queue2.addMessage('LOL')

print(Queue.queues)
Queue.write()
Queue.read()
print(Queue.queues)



topic = Topic('Beach', user1.ID)
topic.addQueue(queue1.ID)

print(Topic.topics)
Topic.write()
Topic.read()
print(Topic.topics)
