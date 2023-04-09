from concurrent import futures
import grpc
from .services.ReplicationService import ReplicationService
from .generated.replication import Replication_pb2_grpc
from .services.UpdateService import UpdateService
from .generated.update import Update_pb2_grpc
from config import GRPC_SERVER_PORT, SERVER_ADDRESS


def serveGRPC():    
    # Creating the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Adding ReplicationService to the server
    Replication_pb2_grpc.add_ReplicationServiceServicer_to_server(ReplicationService(), server)
    # Adding UpdateService to the server
    Update_pb2_grpc.add_UpdateServiceServicer_to_server(UpdateService(), server)

    # Starting the server
    print(f'GRPC server is listening on {SERVER_ADDRESS}:{str(GRPC_SERVER_PORT)}')
    server.add_insecure_port(SERVER_ADDRESS + ":" + str(GRPC_SERVER_PORT))
    server.start()
    server.wait_for_termination()