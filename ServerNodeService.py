import rpyc
from rpyc.utils.server import ThreadedServer
import datetime
import node
date_time=datetime.datetime.now()

class ServerNodeService(rpyc.Service):
  stat = False
  Processes = []

  def __init__(self, node) -> None:
      self.node = node
      #print('hello', node.port)
      super().__init__()

  def exposed_SetNeighbours(self, neighbours):
    self.node.setNeighbours(neighbours)

  def exposed_GetNeighbours(self):
    return self.node.getNeighbours()
  
  def ResetNeighbours(self,nodes):
    return self.node.resetNeighbours(nodes)  
  
  def RemoveNeighbours(self):
    return self.node.removeNeighbours() 
  
  # status stuff
  def exposed_GetAllStatus(self):
    return self.node.getAllStatus()

  def exposed_GetStatus(self):
    return self.node.getStatus()

  # status change stuff 
  def exposed_GatherForStatusChange(self,index,st):
    return self.node.gatherForStatusChange(index,st)
  
  def exposed_StatusChange(self,index,st,was_changed):
    return self.node.statusChange(index,st,was_changed)
  
  # ordering stuff
  def exposed_GatherForOrder(self, order):
    return self.node.gatherForOrder(order)
  
  def exposed_GetOrder(self, order, sender):
    return self.node.getOrder(order, sender)
  
  def exposed_SetOrder(self, order):
    return self.node.setOrder(order)
  
  def exposed_SendOrderToEveryone(self, order):
    return self.node.sendOrderToEveryone(order)
  
  def exposed_AgreeOnOrder(self):
    return self.node.agreeOnOrder()
  
  def exposed_OrderToSend(self,order):
    return self.node.orderToSend(order)
  
  def exposed_CommitToOrder(self):
    return self.node.commitToOrder()
  
  def exposed_OrderInfo(self):
    return self.node.orderInfo()
  
  def exposed_GetId(self):
    return self.node.getId()
  
  
    