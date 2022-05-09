from click import command
import rpyc
import sys
import random as rand

from sympy import true
from node import Node
 
N = 4#int(sys.argv[1])
PORT = 18812
primary = 1 #rand.randint(0, N-1)
nodes = {}


# create nodes
for i in range(1,N+1):
    node = Node(PORT + i, i, PORT + 1)
    node.run()
    nodes[i] = node.port
    lastport = PORT + i

print('all node started', nodes[primary])

conn = rpyc.connect("localhost", port=nodes[primary])
conn.root.SetNeighbours(nodes)
conn.close()

# add node stuff
def addNode(N,lastport):
    for i in range(1, N+1):
        node = Node(lastport + i, i, nodes[primary])
        node.run()
        nodes[i] = node.port
        lastport = lastport + i
    
    conn = rpyc.connect("localhost", port=nodes[primary])
    conn.root.ResetNeighbours(nodes)
    conn.close()

# command loop

while true:
    command = input("\nCommand please: ")

    if "g-state" in command: 
        command = command.split(" ")
        
        if len(command) == 1: # status command
            conn = rpyc.connect("localhost", port=nodes[primary])
            conn.root.GetAllStatus()
            conn.close()
            continue
        
        
        if len(command) == 3: # state change command
            try:
                changed = False
                index = int(command[1])
                st = command[2]
                if st == "faulty" or st == "not_faulty":
                    conn = rpyc.connect("localhost", port=nodes[primary])
                    changed = conn.root.GatherForStatusChange(index,st)
                    conn.close() 
                    if changed:
                        print(f'node {index} was changed to {st}')
                    else:
                        print(f'There is no node {index}')
                        
                    conn = rpyc.connect("localhost", port=nodes[primary])
                    conn.root.GetAllStatus()
                    conn.close()
                else:
                    print("unknown command: try g-state faulty or g-state not_faulty ")
            except:
                print('Error')
        else:
            print("unknown command")  
            
    elif "actual-order" in command: # order command
        try:
            command = command.split(" ")
            order = command[1]
            if command[1] == "attack" or command[1] == "retreat":
                conn = rpyc.connect("localhost", port=nodes[primary])
                changed = conn.root.GatherForOrder(order)
                conn.close()
            else:
                print("unknown command: try actual-order or retreat")
            
        except:
            raise
            
    elif command == "exit":
        print("exiting")
        sys.exit()
        
    elif "add" in command:
        command = command.split(" ")
        n = int(command[1])
        addNode(n,lastport)

    elif "g-kill" in command:
        id = int(command.split(' ')[1])
        
        conn = rpyc.connect("localhost", port=nodes[id])
        conn.root.Kill()
        conn.close()

        if(id in nodes):
            nodes.pop(id)
        if(id == primary):
            primary = min(nodes.keys())
        print(primary, nodes)
        
        conn = rpyc.connect("localhost", port=nodes[primary])
        conn.root.SetNeighbours(nodes)
        conn.root.SetPrimary(nodes[primary])
        print(conn.root.GetNeighbours())
        conn.close()
        
    else:
        print("unknown command")
        
        

    

        



 
 