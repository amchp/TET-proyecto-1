from generated.replication import Replication_pb2, Replication_pb2_grpc
import grpc, json
from google.protobuf.json_format import MessageToDict
from config import MOM_INSTANCES, BASE_DIR


def replicate(filename):
    # Get the JSON and encode it to bytes   
    with open(f'{BASE_DIR}/models/persistence/files/{filename}', 'r') as f:
        data = json.load(f)
        data = json.dumps(data, indent=4) 
        data = data.encode('utf-8')
        
    # Replicate to other MOM instances
    for instance in MOM_INSTANCES:
        with grpc.insecure_channel(instance) as channel:
            stub = Replication_pb2_grpc.ReplicationServiceStub(channel)
            response = stub.replicate(Replication_pb2.Json(data=data, filename=filename))
            response_dict = MessageToDict(response, preserving_proto_field_name=True)
            
            print(f'GRPC-REPLICATION-SERVICE({instance}): {response_dict["message"]}')
