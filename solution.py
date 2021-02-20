# import socket module
from socket import *
import  sys  # In order to terminate the pr


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))
    # Fill in start
    serverSocket.listen(1)
    # Fill in end

    while True:
        # Establish the connection
        #print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()


        try:
            message = connectionSocket.recv(1024)
            # Fill in start    #Fill in end
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()



            # Send one HTTP header line into socket
            # Fill in start
            # Need to send a http header
            connectionSocket.send('HTTP/1.0 200 OK\r\n'.encode())
        # connectionSocket.send(outputdata) #notsure if this is needed. 

        # Fill in end

        # Send the content of the requested file to the client

            for i in range(0, len(outputdata)):

             connectionSocket.send(outputdata[i].encode())  # needs to be encoded see above for how to encode


             connectionSocket.send("\r\n".encode()) #this is needed dont comment out

             connectionSocket.close()

        except IOError:

# Send response message for file not found (404)
# Fill in start

# print '404 Not Found'
             connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())  # need the encode statement here

# Fill in end

# Close client socket
# Fill in start
             connectionSocket.close()
# Fill in end
        serverSocket.close()
        sys.exit()  # Terminate the program after sending the corresponding data

    if __name__ == "__main__":
        webServer(13331)

