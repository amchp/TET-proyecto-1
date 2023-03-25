import uuid
from models.persistence.DatabaseInterface import Types
from models.Queue import Queue
from models.User import User
from models.persistence.Database import FileDatabase


class Topic:
    topics = {}
    def __init__(
            self,
            name: str,
            creator_id: str,
            queues: list = [],
            id: str = None
    ) -> None:
        if id is None:
            self.ID = str(uuid.uuid3(
                uuid.NAMESPACE_OID, f'{name} {creator_id}')
            )
        else:
            self.ID = id
        self.name = name
        self.creator_id = creator_id
        self.queues = queues
        Topic.topics[self.ID] = self

    def update(self, name: str, creator_id: str) -> None:
        self.name = name
        self.creator_id = creator_id

    def addQueue(self, queue_id: str) -> None:
        self.queues.append(queue_id)

    @staticmethod
    def updateTopics(topics) -> None:
        # TODO grab a leader update and update topics
        pass

    @staticmethod
    def read() -> None:
        Topic.topics = {}
        topics = FileDatabase.read(Types.topic)
        for _, topic in topics.items():
            Topic.topics[topic['ID']] = Queue(
                topic['name'],
                topic['creator_id'],
                topic['queues'],
                topic['ID']
            )

    @staticmethod
    def write() -> None:
        FileDatabase.write(Types.topic, Topic.topics)
