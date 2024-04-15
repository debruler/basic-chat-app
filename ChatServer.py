# Isabelle deBruler

from datetime import datetime
from socket import *
import sys
from threading import Thread
import json

# '127.0.0.1'

def strDateTime():
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

def receiveClientMessages(connectionSocket, addr):
    while True:
        # receive single message from client
        clientMessage = connectionSocket.recv(1024)
        if not clientMessage:
            break
        clientMessage = clientMessage.decode()
        clientMessageJSON = json.loads(clientMessage)

        if clientMessageJSON["type"] == "nickname":
            clientInfo.append({
                "nickname": clientMessageJSON["nickname"],
                "clientid": clientMessageJSON["clientid"],
                "ip": clientMessageJSON["ip"],
                "port": clientMessageJSON["port"]
            })
            print(strDateTime() + " :: " + clientMessageJSON["nickname"] + ": connected.\n")
        elif clientMessageJSON["type"] == "message":
            index = None
            for i, info in enumerate(clientInfo):
                if info["nickname"] == clientMessageJSON["nickname"]:
                    index = i
                    break
            # broadcast message to other clients
            if index is not None:
                print("Received: IP: " + clientInfo[index]["ip"] + " Port: " + str(clientInfo[index]["port"]) + " Client-Nickname: " + clientInfo[index]["nickname"] + " Date/Time: " + strDateTime())
                # broadcast message to other clients
                index2 = 0;
                broadcastMsg = ""
                for client in clients:
                    if client != connectionSocket:
                        client.send(clientMessage.encode())
                        broadcastMsg += clientInfo[index2]["nickname"]
                    index2 =+ 1
            print("Broadcasted: " + broadcastMsg)
        elif clientMessageJSON["type"] == "disconnect":
            clients.remove(connectionSocket) 
            for thisClientInfo in clientInfo:
                if thisClientInfo["clientid"] == clientMessageJSON["clientid"]:
                    clientInfo.remove(thisClientInfo)
            connectionSocket.close()

args = sys.argv
if len(args) != 2:
    print ("Usage: python3 TCPServer.py port")
    exit()
elif int(args[1]) >= 65536 or args[1] < 0:
    print("ERR - arg 1")
    exit()

port = int(args[1])
hostname = '127.0.0.1'

welcomeSocket = socket(AF_INET, SOCK_STREAM)
try:
    welcomeSocket.bind((hostname, port))
except Exception as e:
    print("ERR - cannot create ChatServer socket using port number " + str(port))
    exit()

welcomeSocket.listen(5)

print("ChatServer started with server IP: " + hostname + ", port: " + str(port) + "...")

clients = []
clientInfo = []

while True:
    (connectionSocket, addr) = welcomeSocket.accept()
    clients.append(connectionSocket)
    initialMessage = ""
    thread = Thread(target=receiveClientMessages, args=(connectionSocket, addr))
    thread.start()