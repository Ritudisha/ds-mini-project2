import rpyc
import sys
import random as rand
from node import Node
 
N = 4 #sys.argv[1]
PORT = 18812
primary = 0#rand.randint(0, N-1)
nodes = []

#try:
for i in range(1,N+1):
    node = Node(PORT + i, i, primary + 1)
    node.run()
    nodes.append(node.port)

print('all node started', nodes[primary])
#print([p.port for p in nodes], nodes[primary].port)

conn = rpyc.connect("localhost", port=nodes[primary])
conn.root.SetNeighbours(nodes)
print(conn.root.GetNeighbours())
print(conn.root.GetAllStatus())
    

   
# except:
#    raise Exception("Fail")



 
 