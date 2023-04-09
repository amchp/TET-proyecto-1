from abc import ABC, abstractmethod

class Types:
    user='user'
    queue='queue'
    topic='topic'

class DatabaseInterface(ABC):
    @staticmethod
    @abstractmethod
    def read(type : Types) -> dict:
        # TODO read updates from memory
        pass
    
    
    @staticmethod
    @abstractmethod
    def write(type: Types, items: dict) -> None:
        # TODO write persistent information to memeory
        pass
    
    
    @staticmethod
    @abstractmethod
    def replicate(type: Types) -> None:
        # TODO replicate data to other MOM instances
        pass
