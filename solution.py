#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a sever socket
    serverSocket.bind(("", port))
    #Fill in start
    serverSocket.bind((”,serverPort))
    serverSocket.listen(1)
    #print ‘Ready to serve…’
    connectionSocket, addr = serverSocket.accept
    #Fill in end

    while True:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = (13331)
        serverSocket.accept()
        #Fill in start      #Fill in end
        try:
            message = ()
            #Fill in start    #Fill in end
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = ()
            #Fill in start     #Fill in end

            #Send one HTTP header line into socket
            #Fill in start
            connectionSocket.send('\HTTP/1.1 200 OK\r\n\r\n'.encode())
            connectionSocket.send(outputdata)
            connectionSocket.close()

            #Fill in end

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            pass
            
            #Send response message for file not found (404)
            #Fill in start

            #print '404 Not Found'
            connectionSocket.send('\HTTP/1.1 404 Not Found\n\n')

            #Fill in end

            #Close client socket
            #Fill in start

            #Fill in end
            
         break
     pass

    #serverSocket.close()
    #sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
