from grpcmodule.generated.replication import Replication_pb2, Replication_pb2_grpc
from grpcmodule.generated.update import Update_pb2, Update_pb2_grpc
from grpcmodule.parser.JSONParser import bytesToJSON, JSONToBytes
import grpc, json
from google.protobuf.json_format import MessageToDict
from config import MOM_INSTANCES, BASE_DIR, GRPC_TIMEOUT


def replicate(filename):
    # Get the JSON and encode it to bytes   
    with open(f'{BASE_DIR}/models/persistence/files/{filename}', "r") as f:
        data = json.load(f)
        data = JSONToBytes(data)
        
    # Replicate to other MOM instances
    for instance in MOM_INSTANCES:
        try :
            with grpc.insecure_channel(instance) as channel:
                stub = Replication_pb2_grpc.ReplicationServiceStub(channel)
                response = stub.replicate(Replication_pb2.Json(data=data, filename=filename), timeout=GRPC_TIMEOUT)
                response_dict = MessageToDict(response, preserving_proto_field_name=True)
                
                print(f'GRPC-REPLICATION-SERVICE({instance}): {response_dict["message"]}')
        except grpc.RpcError as e:
            print(f'GRPC-REPLICATION-SERVICE({instance}): {e}')
        except Exception as e:
            print(f'GRPC-REPLICATION-SERVICE({instance}): {e}')
        

def update():
    # Getting the MOM instance with the highest log file
    max_log = log()
    
    count    = max_log[0]
    instance = max_log[1]
    
    filename = f'{BASE_DIR}/models/persistence/files/log.json'
    try:            
        with open(filename, "r") as f:
            log_data = json.load(f)
            countLog = log_data['count']
            
    except FileNotFoundError:    
        log_data = {
            "count": 0        
        }
            
        with open(filename, "w+") as f:
            json.dump(log_data, f, indent=4)
            f.seek(0)
            log_data = json.load(f)
            countLog = log_data['count']
    
    # Check if the highest log file is None
    if instance is None:
        print(f'GRPC-UPDATE-SERVICE: No log file received, aborting update')
        return
    
    # Check if the highest log file is from this MOM instance                    
    if count == countLog:
        print(f'GRPC-UPDATE-SERVICE: This MOM instance is up to date, aborting update')
        return
        
    if count < countLog:
        print(f'GRPC-UPDATE-SERVICE: This MOM instance has the highest log file, aborting update')
        return
  
    
    print(f'GRPC-UPDATE-SERVICE({instance}): MOM instance with the highest log file')

    with grpc.insecure_channel(instance) as channel:
        try:
            stub = Update_pb2_grpc.UpdateServiceStub(channel)
            response = stub.update(Update_pb2.Request(), timeout=GRPC_TIMEOUT)
            response_dict = MessageToDict(response, preserving_proto_field_name=True)
            
            # Check if the response is successful
            if(response_dict['is_successful'] == False):
                print(f'GRPC-UPDATE-SERVICE({instance}): Something went wrong')
                return
                        
            # Get the queue_data and decode it to json
            queue_data = bytesToJSON(response_dict['queue_data'])
            
            # Get the users_data and decode it to json
            users_data = bytesToJSON(response_dict['users_data'])
            
            # Get the topic_data and decode it to json
            topic_data = bytesToJSON(response_dict['topic_data'])
            
            # Get the log_data and decode it to json
            log_data = bytesToJSON(response_dict['log_data'])
            
            # Save the files
            with open(f'{BASE_DIR}/models/persistence/files/queue.json', "w") as f:
                json.dump(queue_data, f, indent=4)
                print(f'GRPC-UPDATE-SERVICE({instance}): Queue file received')
                
            with open(f'{BASE_DIR}/models/persistence/files/user.json', "w") as f:
                json.dump(users_data, f, indent=4)
                print(f'GRPC-UPDATE-SERVICE({instance}): Users file received')
                
            with open(f'{BASE_DIR}/models/persistence/files/topic.json', "w") as f:
                json.dump(topic_data, f, indent=4)
                print(f'GRPC-UPDATE-SERVICE({instance}): Topic file received')
                
            with open(f'{BASE_DIR}/models/persistence/files/log.json', "w") as f:
                json.dump(log_data, f, indent=4)
                print(f'GRPC-UPDATE-SERVICE({instance}): Log file received')
                
            print(f'GRPC-UPDATE-SERVICE({instance}): MOM instance updated successfully')
        except grpc.RpcError as e:
            print(f'GRPC-UPDATE-SERVICE({instance}): {e}')
            return


def log():
    # Asking for the log file to other MOM instances
    
    # max_log is a tuple where the first element is the
    # count and the second element is MOM instance address

    max_log = (0, None) 
    
    for instance in MOM_INSTANCES:
        with grpc.insecure_channel(instance) as channel:
            try:
                print(f'GRPC-UPDATE-SERVICE({instance}): Asking for log file')
                stub = Update_pb2_grpc.UpdateServiceStub(channel)
                response = stub.log(Update_pb2.Request(), timeout=GRPC_TIMEOUT)
                response_dict = MessageToDict(response, preserving_proto_field_name=True)
                
                # Check if the response is successful
                if response_dict['is_successful'] == False:
                    print(f'GRPC-UPDATE-SERVICE({instance}): Something went wrong')
                    continue
                            
                # Get the data and decode it to json
                data = bytesToJSON(response_dict['data'])
                
                # Get the count
                count = data['count']
                
                if count > max_log[0]:
                    max_log = (count, instance)
                
                print(f'GRPC-UPDATE-SERVICE({instance}): Log file received')
            except grpc.RpcError as e:
                print(f'GRPC-UPDATE-SERVICE({instance}): {e}')
                continue
    
    return max_log
    
