from socket import *
import sys

def Get(message):
    # Extract the filename from the given message
    # .partition("/")[2]
    #print(message.split()[1].partition("/")[2])
    filename = message.split()[1]
    print (filename)
    fileExist = "false"
    # filetouse = "/" + filename
    try:
        # Check wether the file exist in the cache
        f = open(filename[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message

        tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n", 'utf-8'))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
        for i in range(0, len(outputdata)):
            tcpCliSock.send(bytes(outputdata[i], 'utf-8'))
            print ('Read from cache')
        print(fileExist)

    # Error handling for file not found in cache
    except IOError:
        tcpCliSock.send(bytes("HTTP/1.0 404 sendErrorErrorError\r\n", 'utf-8'))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
        tcpCliSock.send(bytes("\r\n", 'utf-8'))

        tcpCliSock.send(bytes("<html><head></head><body><h1 style='margin: auto auto;'>404 Not Found</h1></body></html>\r\n", 'utf-8'))


def Post(message):
    anwser = message.decode().split("\n")[-1]
    print("\n\n\n",anwser,"\n\n")
    tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n", 'utf-8'))
    tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
    print("ok: post")


if (len(sys.argv)<= 1):
    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip\
: It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) ## I the port is in use this instruction will and
                                                                  # the process in the port to make it able to be use
tcpSerSock.bind((sys.argv[1], 3001))
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