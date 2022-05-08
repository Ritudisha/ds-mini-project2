from http import server
import socket
import time
import threading
from ServerNodeService import ServerNodeService
from multiprocessing import Process
from rpyc.utils.server import ThreadedServer
import rpyc
"""
We used an example p2p network as a starting point to build the DHT: https://github.com/macsnoeren/python-p2p-network
This is a node class that represents a node in DHT.
Each node has a connection to their successor and an id for next successor.

"""

class Node(threading.Thread):

    def __init__(self, port, id, primary):

        super().__init__(daemon=True)

        # When this flag is set, the node will stop and close
        self.id = id
        self.status = 'NF'
        self.primary = primary
        self.neighbours = []
        self.order = 'undefined'

        # currently for local use only
        self.host = "localhost"
        self.port = port
        self.rpcService = ServerNodeService(self)

    def getStatus(self):
        return self.status
    
    def setStatus(self, status):
        self.status = status

    def kill(self):
        return "Not implemeted"

    def addOrder(self, order):
        self.order = order

    def getOrder(self):
        return self.order
    
    def sayHello(self,neighbours):
        print("hello", neighbours)

    def setNeighbours(self, neighbours):
        for neighbour in neighbours:
            if(neighbour == self.port):
                continue
            else:
                self.neighbours.append(neighbour)

        for neighbour in self.neighbours:
                #conn.root.backupNeighbourSet
                conn = rpyc.connect("localhost", neighbour)
                if(len(conn.root.GetNeighbours()) == 0):
                    conn.root.SetNeighbours(neighbours)
                    conn.close()

    

    def getNeighbours(self):
        return self.neighbours

    def run(self):
        
        t=ThreadedServer(self.rpcService, port=self.port)
        thread = threading.Thread(target = start_server, args={t,}, daemon=True)
        
        thread.start()

def start_server(server):
        server.start()

def setNeighbours(self, node, neighbours):
        for neighbour in neighbours:
            if(neighbour.port == self.port):
                continue
            else:
                self.neighbours.add(neighbour)

        #for true_neighbour in self.neighbours:
         #       conn.root.backupNeighbourSet
                conn = rpyc.connect("localhost", neighbour.port)
                if(len(conn.root.getNeighbours()) == 0):
                    conn.root.setNeighbours(neighbour, neighbours)
                    conn.close()

