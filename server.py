import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 65432
messages = []  # list of all the msgs, unnecessary but there anyways
commands = []  # list of all commands to keep track
clients = {}  # dict of all the clients and client numbers
th = []  # all the threads
totalClientNum = 0


def send(msg, clientNumber):  # this sends the msg to all the clients
    msg = ('Client {}: {}'.format(clientNumber, msg.decode())).encode()
    for c in clients.values():
        c.send(msg)



def death_msg(clientNumber):  # sends a msg about client leaving
    msg = ('Client {} has left the chat.'.format(clientNumber)).encode()
    for c in clients.values():
        c.send(msg)


def listen(cli, addr, clientNumber):
    print("Accepted connection from: ", addr)

    while True:
        data = cli.recv(1024)
        if not data:

            break
        else:
            msg = data.decode()
            if msg[0:1] == '/':
                commands.append(msg)
                print(msg[1:])
                if msg[1:8] == 'whisper':  # /whisper 10
                    msg = msg[9:]
                    receiver = int(msg[:msg.find(' ')])
                    msg = ('Client {} to Client {}: {}'.format(clientNumber, receiver, msg[msg.find(' ') + 1:])).encode()
                    clients[receiver].send(msg)
                    cli.send(msg)
                elif msg[1:5] == 'kill':  # /kill
                    for c in clients.values():
                        c.close()
                elif msg[1:5] == 'kick': # /kick 1
                    print('hi')
                    clients[int(msg[6:])].close()
                    print(int(msg[6:]))
            else:
                messages.append(data)
                send(data, clientNumber)
    del clients[clientNumber]
    death_msg(clientNumber)
    cli.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # the bind puts the socket on port 65432 on
    # the specific network interface
    # now listen to the web server on port 65432 - the normal http port
    s.listen(5)
    while True:
        print("Server is listening for connections...")
        client, address = s.accept()
        if len(clients) == 0:
            totalClientNum = 1
            client.send("Welcome to the chat, Client 1! We're glad you could make it!".encode())
        else:
            totalClientNum+=1
            for clie in clients.values():
                clie.send("Client {} has joined the chat".format(totalClientNum).encode())

            client.send("Welcome Client{}".format(totalClientNum).encode())
        clients[totalClientNum] = client

        th.append(Thread(target=listen, args=(client, address,
                                              totalClientNum)).start())  # threaded stuff it makes a thread for each client and makes it do listen


    s.close()
