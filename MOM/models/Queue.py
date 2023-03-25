from collections import deque
import uuid
from models.persistence.Database import FileDatabase
from models.persistence.DatabaseInterface import Types
from models.User import User


class Queue:
    def __init__(
        self,
        creator_id: str,
        receptor_id: str,
        messages: deque = deque(),
        id: str = None
    ) -> None:
        if id is None:
            self.ID = str(uuid.uuid3(
                uuid.NAMESPACE_OID,
                f'{creator_id} {receptor_id}'
            ))
        else:
            self.ID = id
        self.creator_id = creator_id
        self.receptor_id = receptor_id
        self.messages = messages

    def update(self, creator_id: str, receptor_id: str) -> None:
        self.creator_id = creator_id
        self.receptor_id = receptor_id

    def addMessage(self, message: str) -> None:
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
    def updateQueues(queues: dict) -> None:
        # TODO grab a leader update and update queues
        pass

    @staticmethod
    def read() -> dict:
        final_queues = {}
        queues = FileDatabase.read(Types.queue)
        for _, queue in queues.items():
            final_queues[queue['ID']] = Queue(
                queue['creator_id'],
                queue['receptor_id'],
                deque(queue['messages']),
                queue['ID']
            )
        return final_queues

    @staticmethod
    def write(queues: dict) -> None:
        for id, queue in queues.items():
            queue.messages = list(queue.messages)
        FileDatabase.write(Types.queue, queues)
