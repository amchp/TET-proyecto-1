from generated.replication import Replication_pb2, Replication_pb2_grpc
import grpc, os, dotenv, json
from google.protobuf.json_format import MessageToDict


def replicate(filename):
    dotenv.load_dotenv()
    RPC_SERVER_ADDRESS = os.getenv('RPC_SERVER_ADDRESS')
    with grpc.insecure_channel(RPC_SERVER_ADDRESS) as channel:
        stub = Replication_pb2_grpc.ReplicationServiceStub(channel)
    
        # Obtener el json y convertirlo a bytes   
        with open('test.json', 'r') as f:
            data = json.load(f)
            data = json.dumps(data, indent=4) 
            data = data.encode('utf-8')
        
        response = stub.replicate(Replication_pb2.Json(data=data, filename="test.json"))
                    
    response_dict = MessageToDict(response, preserving_proto_field_name=True )
    print(response_dict)