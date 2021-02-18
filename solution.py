#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a server socket
    serverSocket.bind(('', port))  
    #Fill in start
    serverSocket.listen(1)
    #print ‘Ready to serve…’ You can remove this line completley
    #connectionSocket, addr = serverSocket.accept #remove this line, you are calling the same connection socket in line 20
    #Fill in end

    while True:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept() ###()#you dont need the port numbner 13331, the function definition is already setting the port to 13331
        serverSocket.accept() #move this to the "connectionSocket, addr = " this line goes after the = 
        #Fill in start      #Fill in end
        try:
            message = ()#you're missing the rest of the statement here. 
            #Fill in start    #Fill in end
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = () #missing the rest of the statement here
            #Fill in start     #Fill in end

            #Send one HTTP header line into socket
            #Fill in start
            
            connectionSocket.send(outputdata) #notsure if this is needed. 
            #connectionSocket.close() #you dont need this line right now, you are not closing the connection yet.

            #Fill in end

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            
            #Send response message for file not found (404)
            #Fill in start

            #print '404 Not Found'
            connectionSocket.send('\HTTP/1.1 404 Not Found\n\n'.encode())#need the encode statement here

            #Fill in end

            #Close client socket
            #Fill in start
			#need to close the socket here
            connectionSocket.close()
            #Fill in end
            

     serverSocket.close() #Uncomment this out, you need this
     sys.exit()  # Terminate the program after sending the corresponding data #uncomment ths out, you need this

if __name__ == "__main__":
    webServer(13331)


