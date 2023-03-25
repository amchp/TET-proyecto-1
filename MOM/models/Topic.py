import uuid
from models.persistence.DatabaseInterface import Types
from models.Queue import Queue
from models.User import User
from models.persistence.Database import FileDatabase


class Topic:
    def __init__(
            self,
            name: str,
            creator_id: str,
            queues: list = [],
            id: str = None
    ) -> None:
        if id is None:
            self.ID = uuid.uuid3(uuid.NAMESPACE_OID, f'{name} {creator_id}')
        else:
            self.ID = id
        self.name = name
        self.creator_id = creator_id
        self.queues = queues

    def update(self, name: str, creator_id: str) -> None:
        self.name = name
        self.creator_id = creator_id

    def addQueue(self, queue: Queue) -> None:
        self.queues.append(queue)

    @staticmethod
    def updateTopics(topics) -> None:
        # TODO grab a leader update and update topics
        pass

    @staticmethod
    def read() -> dict:
        final_topics = {}
        topics = FileDatabase.read(Types.queue)
        for _, topic in topics.items():
            final_topics[topic['ID']] = Queue(
                topic['name'],
                topic['creator_id'],
                topic['messages'],
                topic['ID']
            )
        return final_topics

    @staticmethod
    def write(topics) -> None:
        FileDatabase.write(Types.topic, topics)
