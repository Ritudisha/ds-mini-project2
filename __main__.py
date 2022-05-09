from click import command
import rpyc
import sys
import random as rand

from sympy import true
from node import Node
 
N = 4 #sys.argv[1]
PORT = 18812
primary = 18813 #rand.randint(0, N-1)
nodes = []

# create nodes
for i in range(1,N+1):
    node = Node(PORT + i, i, primary)
    node.run()
    nodes.append(node.port)

print('all node started', primary)

conn = rpyc.connect("localhost", port=primary)
conn.root.SetNeighbours(nodes)
conn.close()

# print(conn.root.GetNeighbours())


conn = rpyc.connect("localhost", port=primary)
changed = conn.root.GatherForStatusChange(1,"faulty")
conn.close() 

# conn = rpyc.connect("localhost", port=primary)
# changed = conn.root.GatherForStatusChange(3,"faulty")
# conn.close() 


conn = rpyc.connect("localhost", port=primary)
conn.root.GetAllStatus()
conn.close()


conn = rpyc.connect("localhost", port=primary)
conn.root.exposed_GatherForOrder("attack")
conn.close()

    
# command loop

# while true:
#     command = input("\nCommand please: ")
    
#     if command == "g-state":
#         conn = rpyc.connect("localhost", port=nodes[primary])
#         conn.root.GetAllStatus()
#         conn.close()
        
#     elif "g-state" in command:
        
#         try:
#             changed = False
#             command = command.split(" ")
#             index = int(command[1])
#             st = command[2]
#             conn = rpyc.connect("localhost", port=nodes[primary])
#             changed = conn.root.GatherForStatusChange(index,st)
#             conn.close() 
#             if changed:
#                 print(f'node {index} was changed to {st}')
#             else:
#                 print(f'There is no node {index}')
                
#             conn = rpyc.connect("localhost", port=nodes[primary])
#             conn.root.GetAllStatus()
#             conn.close()
                
#         except:
#             print("unknown command")
            
            
#     elif "actual-order" in command:
#         try:
#             command = command.split(" ")
#             order = command[1]
#             conn = rpyc.connect("localhost", port=nodes[primary])
#             changed = conn.root.GatherForOrder(order)
#             conn.close() 
            
#         except:
#             print("unknown command")
        
#     else:
#         print("unknown command")
        
        



 
 