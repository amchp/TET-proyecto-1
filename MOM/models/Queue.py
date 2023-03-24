from collections import deque
from models.User import User


class Queue:
    next_id = 1
    def __init__(self, creator: User, receptor: User) -> None:
        self.ID = Queue.next_id
        Queue.next_id += 1
        self.creator = creator
        self.receptor = receptor
        self.messages = deque()

    def update(self, creator: User, receptor: User) -> None:
        self.creator = creator
        self.receptor = receptor
    
    def addMessages(self, message: str) -> None:
        self.messages.append(message)

    def sendMessages(self) -> None:
        last_message_index = -1
        for i, message in enumerate(self.messages):
            if self.sendMessage(message) < 0:
                break
            last_message_index = i
        for i in range(last_message_index + 1):
            self.messages.popleft()

    def sendMessage(self, message) -> None:
        # TODO gRPC or REST
        pass

    @staticmethod
    def updateQueues(self, queues) -> None:
        # TODO grab a leader update and update queues
        pass
    
    @staticmethod
    def read(self):
        # TODO read updates from memory
        pass

    @staticmethod
    def write(self, queues) -> None:
        # TODO write persistent information to memeory
        pass

