#By - Harsahib Matharoo

import socket
import threading
from datetime import datetime


#name of the pc host and also the port
HOST='127.0.0.1'
PORT= 9090

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()# start listening for TCP connections made to this socket

nowt = datetime.now()
current_timet = nowt.strftime("%H:%M:%S")

all_clients=[]#stores all clients
names=[]#stores all names of all clients

def broadcast(message):#this function forwards every message to all all_clients
    for client in all_clients:
        client.send(message)

def book_cl(client):#This function is called in a different thread for every client incoming ,handles client for communicating.
    while True:
        try:
            message=client.recv(1024)
            #print(f"{names[all_clients.index(client)]} says {message}")
            broadcast(message)
        except:#THis exception is enforced when a certain client closes the chatapp (socket).

            #find the index of that client and remove that client from the list of all clients
            index=all_clients.index(client)
            all_clients.remove(all_clients[index])
            name=names[index]
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            broadcast(f"SERVER: {name} has lost the server at the time {current_time}!. TOTAL CHATTERS:{len(all_clients)}\n".encode('utf-8'))

#remove the name of the clients that have left
            names.remove(name)
            break
def receive():#Receive the relative connection requests and put every single client in a different thread.
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        (client,address) = server.accept()

#add the new client onto the client list
        all_clients.append(client)
        print(f"The client is now Connected with the address of: {str(address)}!")
       
        client.send(("SERVER_CHECK").encode('utf-8'))
        name=client.recv(1024)

        print(f"SERVER : {name} joined the server at {current_time}!. TOTAL CHATTERS:{len(all_clients)}\n".encode('utf-8'))
        broadcast(f"SERVER : {name} joined the server at {current_time}!. TOTAL CHATTERS:{len(all_clients)}\n".encode('utf-8'))

        thread=threading.Thread(target=book_cl,args=(client,))# This is for to correctly handle each single client in distinct thread.
        thread.start()

print(" Welcome to the H.M Chat App \n")
print("Server is now Active at......", current_timet, "\n")

print("Log in as a client and start chatting with other clients!.")
receive()

