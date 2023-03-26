import uuid, hashlib
from models.Queue import Queue
from models.persistence.DatabaseInterface import Types
from models.persistence.Database import FileDatabase


class User:
    users = dict()
    def __init__(self, name: str, password: str, id: str = None, queues: dict = None) -> None:
        if id is None:
            self.ID = str(uuid.uuid3(uuid.NAMESPACE_OID, name))
            if self.ID in User.users:
                raise Exception('User already exist')
        else:
            self.ID = id
        self.name = name
        self.password = password #hashlib.sha256(password.encode('ascii')).hexdigest()
        if queues is None:
            self.queues = {}
        else:
            self.queues = queues
        User.users[self.ID] = self

    def addQueue(self, queue_id : str) -> None:
        self.queues[queue_id] = queue_id

    def deleteQueue(self, queue_id) -> None:
        del self.queues[queue_id]

    def getMessages(self):
        messages = []
        for queue_id in self.queues.keys():
            messages += Queue.queues[queue_id].sendMessages()
        return messages
    
    def delete(self):
        del User.users[self.ID]
        del self

    @staticmethod
    def list():
        return User.users.values()

    @staticmethod
    def find(name: str):
        User.users[str(uuid.uuid3(
            uuid.NAMESPACE_OID,
            f'{name}'
        ))]

    @staticmethod
    def read() -> None:
        User.users = {}
        users = FileDatabase.read(Types.user)
        for _, user in users.items():
            User.users[user['ID']] = User(
                user['name'],
                user['password'],
                user['ID'],
                user['queues']
            )

    @staticmethod
    def write() -> None:
        FileDatabase.write(Types.user, User.users)
