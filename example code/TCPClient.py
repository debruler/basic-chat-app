# TCPClient.py

from socket import *
import sys

args = sys.argv
if len(args) != 3:
    print ("Usage: python3 TCPClient.py hostname port")
    exit()
hostname = args[1]
port = int(args[2])

# Create socket and connect to server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((hostname, port))

# Read line from user
clientSentence = input('Client ready for input\n')

# Write line to server
clientSocket.send(clientSentence.encode())
print ('TO SERVER:', clientSentence)

# Read line from server
serverSentence = clientSocket.recv(1024)
serverSentence = serverSentence.decode()
print ('FROM SERVER:', serverSentence)

# Close the socket
clientSocket.close()
