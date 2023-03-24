from models.Queue import Queue
from models.User import User


class Topic:
    next_id = 1
    def __init__(self, name : str, creator : User) -> None:
        self.ID = Topic.next_id
        Topic.next_id += 1
        self.name = name
        self.creator = creator
        self.queues = []

    def update(self, name: str, creator: User) -> None:
        self.name = name
        self.creator = creator

    def addQueue(self, queue: Queue) -> None:
        self.queues.append(queue)
        
    @staticmethod
    def updateTopics(self, topics) -> None:
        # TODO grab a leader update and update topics
        pass
    
    @staticmethod
    def read(self):
        # TODO read persistent information from memory
        pass

    @staticmethod
    def write(self, topics) -> None:
        # TODO write persistent information to memeory
        pass
