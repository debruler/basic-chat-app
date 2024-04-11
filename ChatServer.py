from socket import *
import sys

args = sys.argv
if len(args) != 2:
    print ("Usage: python3 TCPServer.py port")
    exit()
elif args[1] >= 65536:
    print("ERR - arg " + args[1])
    exit()

port = int(args[1])
ip = 0 #idk where to get IP address hehe
# come back here ^^^^^^

# what are the params here.........
welcomeSocket = socket(AF_INET, SOCK_STREAM)
try:
    welcomeSocket.bind((ip, port))
except welcomeSocket.error as e:
    print("ERR - cannot create ChatServer socket using port number " + port)
    exit()
#idk if this is how try catch blocks work ^^^

welcomeSocket.listen(1)

print("ChatServer started with server IP: " + ip + ", port: " + port + "...")

while(True):
    (connectionSocket, addr) = welcomeSocket.accept()
    