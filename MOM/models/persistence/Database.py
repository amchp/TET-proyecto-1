import json
from models.persistence.DatabaseInterface import Types
from models.persistence.Log import updateLog 
from config import BASE_DIR
from grpcmodule.GRPCClient import replicate


class FileDatabase():
    file_names = {
        Types.user: 'user.json',
        Types.topic: 'topic.json',
        Types.queue: 'queue.json'
    }

    @staticmethod
    def read(type) -> dict:
        items = {}
        with open(f'{BASE_DIR}/models/persistence/files/{FileDatabase.file_names[type]}', 'r') as file:
            items = json.load(file)
        return items

    @staticmethod
    def write(type, items) -> None:       
        with open(f'{BASE_DIR}/models/persistence/files/{FileDatabase.file_names[type]}', 'w') as file:
            # store data into the disk
            file.write(json.dumps(
                items,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4
            ))
            
            file.close()
            
            
            # Updating log.json file
            updateLog()

            # replicate data to other MOM instances
            replicate(FileDatabase.file_names[type])
            
