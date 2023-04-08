import uuid
from models.Queue import Queue
from models.persistence.DatabaseInterface import Types
from models.persistence.Database import FileDatabase
from threading import Lock


class Topic:
    topics = {}
    lock = Lock()

    def __init__(
            self,
            name: str,
            queues: dict = None,
            subscribers: dict = None,
            id: str = None
    ) -> None:
        if id is None:
            self.ID = str(uuid.uuid3(
                uuid.NAMESPACE_OID, f'{name}')
            )
            if self.ID in Topic.topics:
                raise Exception('Topic already exist')
        else:
            self.ID = id
        self.name = name
        if queues is None:
            self.queues = {}
        else:
            self.queues = queues
        if subscribers is None:
            self.subscribers = {}
        else:
            self.subscribers = subscribers
        Topic.topics[self.ID] = self

    def addQueue(self, queue_id: str) -> None:
        self.queues[queue_id] = queue_id

    def deleteQueue(self, queue_id: str):
        del self.queues[queue_id]

    def createQueuesForSubscribers(self, creator_id):
        for receptor_id in self.subscribers.keys():
            queue = Queue.findOrCreate(creator_id, receptor_id)
            self.addQueue(queue.ID)

    def addMessage(self, creator_id, message):
        self.createQueuesForSubscribers(creator_id)
        for queue_id in self.queues.keys():
            Queue.queues[queue_id].addMessage(message)

    def addSubscriber(self, user_id: str) -> None:
        self.subscribers[user_id] = user_id

    def deleteSubscriber(self, user_id: str):
        del self.subscribers[user_id]

    def delete(self):
        del Topic.topics[self.ID]
        del self

    @staticmethod
    def attributesToId(name: str):
        return str(uuid.uuid3(uuid.NAMESPACE_OID, name))

    @staticmethod
    def list():
        return Topic.topics.values()

    @staticmethod
    def find(name: str):
        Topic.topics[str(uuid.uuid3(
            uuid.NAMESPACE_OID,
            f'{name}'
        ))]

    @staticmethod
    def read() -> None:
        Topic.topics = {}
        topics = FileDatabase.read(Types.topic)
        for _, topic in topics.items():
            Topic.topics[topic['ID']] = Topic(
                topic['name'],
                topic['queues'],
                topic['subscribers'],
                topic['ID']
            )

    @staticmethod
    def write() -> None:
        FileDatabase.write(Types.topic, Topic.topics)
