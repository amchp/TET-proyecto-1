import uuid
from models.persistence.Database import FileDatabase
from models.persistence.DatabaseInterface import Types
from util.exceptions import DuplicatedQueueException
from threading import Lock

class Queue:
    queues = {}
    lock = Lock()

    def __init__(
        self,
        creator_id: str,
        receptor_id: str,
        messages: list = None,
        id: str = None
    ) -> None:
        with Queue.lock:
            if id is None:
                self.ID = str(uuid.uuid3(
                    uuid.NAMESPACE_OID,
                    f'{creator_id} {receptor_id}'
                ))
                if self.ID in Queue.queues:
                    raise DuplicatedQueueException('Queue already exist')
            else:
                self.ID = id
            self.creator_id = creator_id
            self.receptor_id = receptor_id
            if messages is None:
                self.messages = []
            else:
                self.messages = messages
            Queue.queues[self.ID] = self

    def addMessage(self, message: str) -> None:
        with Queue.lock:
            self.messages.append(message)

    def sendMessages(self) -> list:
        with Queue.lock:
            messages = self.messages.copy()
            self.messages.clear()
            return messages

    def delete(self):
        if len(self.messages):
            raise Exception("Queue isn't empty!")
        with Queue.lock:
            del Queue.queues[self.ID]
            del self

    @staticmethod
    def attributesToId(creator_id: str, receptor_id: str,):
        return str(uuid.uuid3(
            uuid.NAMESPACE_OID,
            f'{creator_id} {receptor_id}'
        ))

    @staticmethod
    def list():
        return Queue.queues.values()

    @staticmethod
    def findOrCreate(creator_id: str, receptor_id: str):
        id = str(uuid.uuid3(
            uuid.NAMESPACE_OID,
            f'{creator_id} {receptor_id}'
        ))
        if id in Queue.queues:
            return Queue.queues[id]
        return Queue(creator_id, receptor_id)

    @staticmethod
    def find(creator_id: str, receptor_id: str,):
        Queue.queues[str(uuid.uuid3(
            uuid.NAMESPACE_OID,
            f'{creator_id} {receptor_id}'
        ))]

    @staticmethod
    def read() -> None:
        Queue.queues = {}
        queues = FileDatabase.read(Types.queue)
        for _, queue in queues.items():
            Queue.queues[queue['ID']] = Queue(
                queue['creator_id'],
                queue['receptor_id'],
                queue['messages'],
                queue['ID']
            )

    @staticmethod
    def write() -> None:
        with Queue.lock:
            FileDatabase.write(Types.queue, Queue.queues)
