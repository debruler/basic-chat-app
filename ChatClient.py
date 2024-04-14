import json
from socket import *
from datetime import datetime
import sys

args = sys.argv

index = 0
hostname = 0
port = 0
nickname = ""
clientid = 0
dateTime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

for arg in args:
    if index + 1 > len(args):
        print("ERR - arg " + index)
    if index == 1:
        hostname = arg
    elif index == 2:
        port = arg
    elif index == 3:
        nickname = arg
    elif index == 4:
        clientid = arg
    index += 1

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((hostname, port))

print("ChatClient started with server IP: " + hostname + ", port: " + port + ", nickname: " + nickname +", client ID: " + clientid, + " Date/Time: " + dateTime)

clientSocket.send(("type: nickname, nickname: " + nickname + ", clientID: " + clientid + ", timestamp: " + dateTime).encode())
# initialMessage = str.encode(json.dumps({
#     "type": "nickname",
#     "nickname": nickname,
#     "clientID" : clientid,
#     "timestamp": dateTime
# }))
# clientSocket.send(initialMessage)

disconnect = False

while not disconnect:
    clientMessage = input('Enter message...\n')
    if (clientMessage == "disconnect"):
        disconnect = True
    else:
        clientSocket.send(("type: message, nickname: " + nickname + ", message: " + clientMessage + ", timestamp: " + dateTime))
        serverSentence = clientSocket.recv(1024)
        serverSentence = serverSentence.decode()
        print(serverSentence)

clientSocket.close()
print("Statistics about chat session...")