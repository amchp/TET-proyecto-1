from concurrent import futures
import grpc, os, dotenv
from services.ReplicationService import ReplicationService
from generated.replication import Replication_pb2_grpc


def serve():
    dotenv.load_dotenv()
    RPC_SERVER_ADDRESS = os.getenv('RPC_SERVER_ADDRESS')
    print(RPC_SERVER_ADDRESS)
    
    # Creating the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Adding ReplicationService to the server
    Replication_pb2_grpc.add_ReplicationServiceServicer_to_server(ReplicationService(), server)

    # Starting the server
    print("Grpc server is running...")
    server.add_insecure_port(RPC_SERVER_ADDRESS)
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()