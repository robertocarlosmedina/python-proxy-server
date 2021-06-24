from socket import *
import json  
import sys

def Get(message):
    # Extract the filename from the given message
    filename = message.split()[1]
    print ("\n[GET Request] \nRequest body: \n", filename, "\n")
    try:
        # Check wether the file exist in the cache
        f = open(filename[1:], "r")
        outputdata = f.readlines()
        # ProxyServer finds a cache hit and generates a response message

        tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n", 'utf-8'))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
        for i in range(0, len(outputdata)):
            tcpCliSock.send(bytes(outputdata[i], 'utf-8'))
        print ('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        tcpCliSock.send(bytes("HTTP/1.0 404 sendErrorErrorError\r\n", 'utf-8'))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
        tcpCliSock.send(bytes("\r\n", 'utf-8'))

        tcpCliSock.send(bytes("<html><head></head><body><h1 style='margin: auto auto;'>404 Not Found</h1></body></html>\r\n", 'utf-8'))


def Post(message):
    try:
        anwser = message.decode().split("\n")[-1]
        anwser = anwser.split("&")
        dictAnswer = {anwser[0].split("=")[0]: anwser[0].split("=")[1],anwser[1].split("=")[0]: anwser[1].split("=")[1] }
        print("\n[POST Request] \nRequest body: ",dictAnswer,"\n")
        tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n", 'utf-8'))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
    except IOError:
        tcpCliSock.send(bytes("HTTP/1.0 404 sendErrorErrorError\r\n", 'utf-8'))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
        tcpCliSock.send(bytes("\r\n", 'utf-8'))


if (len(sys.argv)<= 1):
    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip\
: It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) ## I the port is in use this instruction will and
                                                                  # the process in the port to make it able to be use
tcpSerSock.bind((sys.argv[1], 3002))
tcpSerSock.listen(100)

while 1:
    # Strat receiving data from the client
    print ('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('Received a connection from:'), addr
    message = tcpCliSock.recv(1024)
    print (message)

    method = message.decode().split(" ")[0]
    if method == "GET":
        Get(message)
    elif method == "POST":
        Post(message)
    else:
        print("method is neither GET nor POST")

    tcpCliSock.close()
tcpSerSock.close()