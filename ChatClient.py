import json
from socket import *
from datetime import datetime
import sys

def strDateTime():
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

args = sys.argv
index = 0
hostname = 0
port = 0
nickname = ""
clientid = 0

for arg in args:
    if index + 1 > len(args):
        print("ERR - arg " + index)
    if index == 1:
        hostname = arg
    elif index == 2:
        port = int(arg)
    elif index == 3:
        nickname = arg
    elif index == 4:
        clientid = arg
    index += 1

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((hostname, port))

print("ChatClient started with server IP: " + hostname + ", port: " + str(port) + ", nickname: " + nickname + ", client ID: " + clientid + ", Date/Time: " + strDateTime())

# clientSocket.send(("type: nickname, nickname: " + nickname + ", clientid: " + clientid + ", timestamp: " + strDateTime).encode())
initialMessage = str.encode(json.dumps({
    "type": "nickname",
    "nickname": nickname,
    "clientid" : clientid,
    "ip": hostname,
    "port": port,
    "timestamp": strDateTime()
}))
clientSocket.send(initialMessage)

disconnect = False

while not disconnect:
    clientMessage = input('Enter message:\n')
    if (clientMessage == "disconnect"):
        disconnect = True
        nextMessage = str.encode(json.dumps({
            "type": "disconnect",
            "nickname": nickname,
            "message": clientMessage,
            "timestamp": strDateTime()
        }))
        clientSocket.send(nextMessage)
    else:
        nextMessage = str.encode(json.dumps({
            "type": "message",
            "nickname": nickname,
            "message": clientMessage,
            "timestamp": strDateTime()
        }))
        clientSocket.send(nextMessage)
    serverSentence = clientSocket.recv(1024)
    serverSentence = serverSentence.decode()
    print(serverSentence)

# wait for ack from the server

clientSocket.close()
print("Summary: ")