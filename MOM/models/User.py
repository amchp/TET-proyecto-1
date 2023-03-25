import uuid
from models.persistence.DatabaseInterface import Types
from models.persistence.Database import FileDatabase


class User:
    def __init__(self, name: str, password: str, id: str = None) -> None:
        if id is None:
            self.ID = str(uuid.uuid3(uuid.NAMESPACE_OID, name))
        else:
            self.ID = id
        self.name = name
        self.password = password

    def update(self, name: str, password: str) -> None:
        self.name = name
        self.password = password

    @staticmethod
    def updateTopics(users) -> None:
        # TODO grab a leader update and update topics
        pass

    @staticmethod
    def read() -> dict:
        final_users = {}
        users = FileDatabase.read(Types.user)
        for _, user in users.items():
            final_users[user['ID']] = User(
                user['name'],
                user['password'],
                user['ID']
            )
        return final_users

    @staticmethod
    def write(users) -> None:
        FileDatabase.write(Types.user, users)
