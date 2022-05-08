import rpyc
import sys
 
if len(sys.argv) < 2:
   exit("Usage {} SERVER".format(sys.argv[0]))
 
server = sys.argv[1]

try:
   conn = rpyc.connect(server,18813)
   if(not conn.root.isrunning()):
      n = input('The number of threads: ')
      conn.root.start_processes(n)
      
   cmd = ''
   while(conn.root.isrunning() and cmd != 'exit'):
      print("Input the command")
      cmd = input()
      conn.root.execute_command(cmd)
   
except:
   raise Exception("Fail")



 
 