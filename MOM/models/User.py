class User:
    next_id = 1
    def __init__(self, name: str, password: str) -> None:
        self.ID = User.next_id
        User.next_id += 1
        self.name = name
        self.password = password

    def update(self, name: str, password: str) -> None:
        self.name = name
        self.password = password

    @staticmethod
    def updateTopics(self, users) -> None:
        # TODO grab a leader update and update topics
        pass
    
    @staticmethod
    def read(self):
        # TODO read persistent information from memory
        pass

    @staticmethod
    def write(self, users) -> None:
        # TODO write persistent information to memeory
        pass