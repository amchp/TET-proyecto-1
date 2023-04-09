from config import BASE_DIR
from grpcmodule.generated.update import Update_pb2, Update_pb2_grpc
from grpcmodule.parser.JSONParser import JSONToBytes
import json


class UpdateService(Update_pb2_grpc.UpdateServiceServicer):
    def __init__(self) -> None:
        super().__init__()

    
    def update(self, request, context):
        print(f'GRPC-UPDATE-SERVICE: Update request received')
        try:
            with open(f'{BASE_DIR}/models/persistence/files/queue.json', "r") as f:
                queue_data = json.load(f)
                queue_data = JSONToBytes(queue_data)
            
            with open(f'{BASE_DIR}/models/persistence/files/user.json', "r") as f:   
                users_data = json.load(f)
                users_data = JSONToBytes(users_data)
                
            with open(f'{BASE_DIR}/models/persistence/files/topic.json', "r") as f:   
                topic_data = json.load(f)
                topic_data = JSONToBytes(topic_data)
                
            with open(f'{BASE_DIR}/models/persistence/files/log.json', "r") as f:   
                log_data = json.load(f)
                log_data = JSONToBytes(log_data)
 
        except Exception as e:
            print(f'GRPC-UPDATE-SERVICE: {e}')
            return Update_pb2.UpdateResponse(is_successful=False, users_data=None, queue_data=None, topic_data=None, log_data=None)
        
        print(f'GRPC-UPDATE-SERVICE: Update request successfully completed')
        return Update_pb2.UpdateResponse(is_successful=True, users_data=users_data, queue_data=queue_data, topic_data=topic_data, log_data=log_data)
        
    
    
    def log(self, request, context):
        print(f'GRPC-UPDATE-SERVICE: Log request received')
        filename = f'{BASE_DIR}/models/persistence/files/log.json'
        try:            
            with open(filename, "r") as f:
                data = json.load(f)
                data = JSONToBytes(data)
                
        except Exception as e:
            print(f'GRPC-UPDATE-SERVICE: {e}')
            return Update_pb2.LogResponse(is_successful=False, data=None)
          
        print(f'GRPC-UPDATE-SERVICE: Log request successfully completed')  
        return Update_pb2.LogResponse(is_successful=True, data=data)