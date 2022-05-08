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

  def exposed_GetAllStatus(self):
    return self.node.getNeighboursStatus()

  def exposed_GetStatus(self):
    return self.node.getStatus()