from generated.replication import Replication_pb2, Replication_pb2_grpc
from google.protobuf.json_format import MessageToDict
from dotenv import load_dotenv, dotenv_values
import json, base64


class ReplicationService(Replication_pb2_grpc.ReplicationServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        
        load_dotenv()
        env = dotenv_values("../.env")
        self._MOMInstances = eval(env["MOM_INSTANCES"])

    def replicate(self, request, context):
        try:
            request = MessageToDict(request, preserving_proto_field_name=True)
            # Get the filename
            filename = request['filename']
            
            # Get the data and decode it to json
            data = request['data']
            data = base64.b64decode(data)
            data = json.loads(data)
            data = json.dumps(data, indent=4)

            # Save the file
            with open("../models/persistence/files/" + filename, "w") as f:
                f.write(data)
            
        except Exception as e:
            return Replication_pb2.ReplicateResponse(is_successful=False, message=str(e))
            
        return Replication_pb2.ReplicateResponse(is_successful=True, message="Data replicated successfully")
