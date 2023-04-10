from controllers import UserController, TopicController, QueueController
from bottle import app, run
from bottle_cors_plugin import cors_plugin
from grpcmodule.GRPCServer import serveGRPC
from grpcmodule.GRPCClient import update
from config import SERVER_ADDRESS, REST_SERVER_PORT
from threading import Thread


def updateDatabase():
    update()


def runGRPCServer():
    serveGRPC()
    

def runRESTServer():
    server = app()
    server.install(cors_plugin('*'))
    run(host=SERVER_ADDRESS, port=REST_SERVER_PORT)


if __name__ == '__main__':
    GRPCThread = Thread(target=runGRPCServer)
    RESTThread = Thread(target=runRESTServer)
    updateThread = Thread(target=updateDatabase)
    
    GRPCThread.start()
    
    # Wait for the update thread to finish and then start the REST server
    updateThread.start()
    updateThread.join()
    
    RESTThread.start()
    
