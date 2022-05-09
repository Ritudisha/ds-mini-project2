from http import server
import socket
import time
import threading
import random

from sympy import false, true
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
        self.order_msg = dict()
        

        # currently for local use only
        self.host = "localhost"
        self.port = port
        self.rpcService = ServerNodeService(self)
    
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
        
    def getNeighbours(self):
        return self.neighbours
                      
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
                # print("neighbour",neighbour)
                    
    # get status stuff                       
    def getStatus(self):
        return self.id, self.status

    def getAllStatus(self):
        print(f"G{self.id}, state={self.status}")
        for n in self.neighbours:
            conn = rpyc.connect("localhost", n)
            id,status = conn.root.GetStatus()
            print(f"G{id}, state={status}")
            conn.close()
            
    # status change stuff
    def gatherForStatusChange(self,index,st):
        was_changed = False
        was_changed = self.statusChange(index,st,was_changed)
        for n in self.neighbours:
            conn = rpyc.connect("localhost", n)
            was_changed = conn.root.StatusChange(index,st,was_changed)
            conn.close()
                
        return was_changed
                         
    def statusChange(self,index,st,was_changed):
        if self.id == index:
            if st == "faulty":
                self.status = "F"
            else:
                self.status = "NF"
            return True
        else:
            if was_changed == False:
                return False
            if was_changed == True:
                return True
            
    # order stuff
    def gatherForOrder(self,order):
        self.setOrder(order)
        sender = self.port
        
        for n in self.neighbours:
            order = self.orderToSend(order)
            conn = rpyc.connect("localhost", n)
            conn.root.GetOrder(order,sender)
            conn.root.SendOrderToEveryone(order)
            conn.close()
        
        bad_guys = dict()
        
        for n in self.neighbours: 
            conn = rpyc.connect("localhost", n)
            bad = conn.root.AgreeOnOrder()
            conn.close()
            bad_guys[n] = bad
            
        print(f"G{self.id}, primary, majority={self.order}, state={self.status}")
        orders = dict()
        
        for n in self.neighbours: 
            conn = rpyc.connect("localhost", n)
            conn.root.CommitToOrder()
            conn.close()
            
        return
    
    def getOrder(self, order, sender):
        self.order_msg[sender] = order
        return
    
    def orderToSend(self,order):
        if self.status == "NF":
            return order
        else:
            malice = random.randint(0,1)
            if malice == 0:
                return order
            else:
                if order == "attack":
                    return "retreat"
                else:
                    return "attack"
        
    def setOrder(self, order):
        self.order = order
        return
    
    def sendOrderToEveryone(self,order):
        sender = self.port
        for n in self.neighbours:
            if n == self.primary:
                continue
            else:
                order = self.orderToSend(order)
                conn = rpyc.connect("localhost", n)
                conn.root.GetOrder(order,sender)
                conn.close()
        return    
                
    def agreeOnOrder(self):
        lets_attack_msg = []
        lets_retreat_msg = []
        for general in self.order_msg:
            if self.order_msg[general] == "attack":
                lets_attack_msg.append(general)
            else:
                lets_retreat_msg.append(general)
                
        self.order_msg = dict()
                
        if len(lets_attack_msg) > 0 and len(lets_retreat_msg) > 0:
            if len(lets_attack_msg) == len(lets_retreat_msg):
                self.setOrder("undefined")
                return []
                
            elif len(lets_attack_msg) > len(lets_retreat_msg):
                self.setOrder("attack")
                return lets_retreat_msg
            
            elif len(lets_attack_msg) < len(lets_retreat_msg):
                self.setOrder("retreat")
                return lets_attack_msg
    
        else:
            if len(lets_attack_msg) > 0:
                self.setOrder("attack")
                return []
            
            else:
                self.setOrder("retreat")
                return []
            
    def commitToOrder(self):
        print(f"G{self.id}, secondary, majority={self.order}, state={self.status}")
        return self.order
    
    
    def run(self):
        t=ThreadedServer(self.rpcService, port=self.port)
        thread = threading.Thread(target = start_server, args={t,}, daemon=True)
        
        thread.start()

def start_server(server):
        server.start()

