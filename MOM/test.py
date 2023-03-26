from models.Topic import Topic
from models.Queue import Queue
from models.User import User


user1 = User(name='Alejandro Mc Ewen', password='password')
user2 = User(name='Elisa Rodriguez', password='password')

queue1 = Queue(user1.ID, user2.ID)
user2.addQueue(queue1.ID)
queue2 = Queue(user2.ID, user1.ID)
user1.addQueue(queue2.ID)
user3 = User(name='Juanma', password='password')
queue3 = Queue(user3.ID, user1.ID)
user1.addQueue(queue3.ID)
queue1.addMessage('HI')
queue1.addMessage('BYE')
queue2.addMessage('Cool')
queue2.addMessage('LOL')
queue3.addMessage('AWSOME')
queue3.addMessage('LAST')

# print(User.users)
User.write()
User.read()
# print(User.users)



# print(Queue.queues)
Queue.write()
Queue.read()
# print(Queue.queues)

print(user1.getMessages())
print(user1.getMessages())
print(user2.getMessages())
print(user2.getMessages())

topic = Topic('Beach')
topic.addQueue(queue1.ID)

# print(Topic.topics)
Topic.write()
Topic.read()
# print(Topic.topics)
