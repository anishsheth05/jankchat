
import socket
from threading import Thread
import thread

HOST = '127.0.0.1'
PORT = 80
messages = [] #list of all the msgs, unnecessary but there anyways
clients = [] #list of all the clients
th = [] #all the threads
def send(msg): #this sends the msg to all the clients
  for client in clients:
    clients.send(msg.encode())
    
def listen(client,address): 
   print "Accepted connection from: ", address
    clients.append(client)
    while True:
        data = client.recv(1024)
        if not data:
            break
        else:
            messages.append(data)
            send(data)
    client.close()
            

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # the bind puts the socket on port 80 on
    # the specific network interface
    # now listen to the web server on port 80 - the normal http port
    s.listen(5)
    while True:
       print "Server is listening for connections..."
        client, address = s.accept()
       th.append(Thread(target=listen, args = (client,address)).start()) #threaded stuff it makes a thread for each client and makes it do listen

    s.close()
   
        
      
