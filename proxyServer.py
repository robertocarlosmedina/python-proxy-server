from socket import *
import sys

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
    # Extract the filename from the given message
    print (message.split()[1])
    # .partition("/")[2]
    #print(message.split()[1].partition("/")[2])
    filename = message.split()[1]
    print (filename)
    fileExist = "false"
    # filetouse = "/" + filename
    filetouse = filename
    print (filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
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
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)

            hostn = filename.replace(bytes("www.", 'utf-8'),bytes("", 'utf-8'),1)
            print (hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write(bytes("GET "+"http://" + filename + "HTTP/1.0\n\n", 'utf-8'))

                # Read the response into buffer
                buff = fileobj.readlines()
                # Create a new file in the cache for the
                # requested file. Also send the response in the buffer to client
                # socket and the corresponding file in the cache

                tmpFile = open("./" + filename,"wb")
                for line in buff:
                    tmpFile.write(line);
                    tcpCliSock.send(line);

            except:
                print ("Illegal request")

    else:
            # HTTP response message for file not found
        tcpCliSock.send(bytes("HTTP/1.0 404 sendErrorErrorError\r\n", 'utf-8'))

        tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
        tcpCliSock.send(bytes("\r\n", 'utf-8'))

    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()