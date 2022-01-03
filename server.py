import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 65432
messages = []  # list of all the msgs, unnecessary but there anyways
clients = []  # list of all the clients
th = []  # all the threads


def send(msg, clientNumber):  # this sends the msg to all the clients
    msg = ('Client {}: {}'.format(clientNumber,msg.decode())).encode()
    for c in clients:
        c.send(msg)

def death_msg(clientNumber):    # sends a msg about client leaving
    msg = ('Client {} has left the chat.'.format(clientNumber)).encode()
    for c in clients:
        c.send(msg)

def listen(cli, addr, clientNumber):
    print("Accepted connection from: ", addr)
    clients.append(cli)
    while True:
        data = cli.recv(1024)
        if not data:
            break
        else:
            messages.append(data)
            send(data, clientNumber)
    cli.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # the bind puts the socket on port 65432 on
    # the specific network interface
    # now listen to the web server on port 65432 - the normal http port
    s.listen(5)
    while True:
        print("Server is listening for connections...")
        client, address = s.accept()
        th.append(Thread(target=listen, args=(
        client, address, len(clients)+1)).start())  # threaded stuff it makes a thread for each client and makes it do listen
        for c in clients:
            c.send("Client {} has joined the chat".format(len(clients)+1).encode())


    s.close()
