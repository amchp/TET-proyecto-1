import uuid
import hashlib
from models.Queue import Queue
from models.persistence.DatabaseInterface import Types
from models.persistence.Database import FileDatabase
from util.exceptions import DuplicatedUserException
from threading import Lock

class User:
    users = dict()
    lock = Lock()

    def __init__(self, name: str, password: str, id: str = None, queues: dict = None) -> None:
        with User.lock:
            if id is None:
                self.ID = str(uuid.uuid3(uuid.NAMESPACE_OID, name))
                if self.ID in User.users:
                    raise DuplicatedUserException('User already exist')
            else:
                self.ID = id
            self.name = name
            # hashlib.sha256(password.encode('ascii')).hexdigest()
            self.password = password
            if queues is None:
                self.queues = {}
            else:
                self.queues = queues
            User.users[self.ID] = self

    def addQueue(self, queue_id: str) -> None:
        with User.lock:
            self.queues[queue_id] = queue_id

    def deleteQueue(self, queue_id) -> None:
        with User.lock:
            del self.queues[queue_id]

    def getMessages(self):
        with User.lock:
            messages = []
            for queue_id in self.queues.keys():
                messages += Queue.queues[queue_id].sendMessages()
            return messages

    def delete(self):
        with User.lock:
            del User.users[self.ID]
            del self

    @staticmethod
    def attributesToId(name: str):
        return str(uuid.uuid3(uuid.NAMESPACE_OID, name))

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
        with User.lock:
            FileDatabase.write(Types.user, User.users)
