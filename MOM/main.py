from bottle import run
from grpcmodule.GRPCServer import serveGRPC
from config import SERVER_ADDRESS, REST_SERVER_PORT
from threading import Thread


def runGRPCServer():
    serveGRPC()
    

def runRESTServer():
    run(host=SERVER_ADDRESS, port=REST_SERVER_PORT)


if __name__ == '__main__':
    GRPCThread = Thread(target=runGRPCServer)
    RESTThread = Thread(target=runRESTServer)
    
    RESTThread.start()
    GRPCThread.start()
