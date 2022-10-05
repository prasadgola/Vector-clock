import socket
from _thread import *
#vector for storing the client connections
clients = {}

#Helper Function to handle the client connections
def handle_client(clientSocket, processId):
    #send process to client
    clientSocket.send(str.encode(str(processId)))
    while True:
        #receive incoming event messages from client process
        clientData = clientSocket.recv(2048)
        #decode the message
        clientMessage = clientData.decode('utf-8')
        print("Received Event: " + clientMessage)
        messageList = clientMessage.split(",")
        recipientClient = messageList[1]

        for client in clients:
            # send the received message to corresponding client
            if str(client) == str(recipientClient):
                response = "p:"
                response = response + str(clientMessage)
                print("Sending event message to process " + str(recipientClient))
                clients[client].sendall(str.encode(response))
            else: #broadcast message to all clients to update their clocks
                response = "b:"
                response = response + str(clientMessage)
                print("Sending broadcast message to process " + str(client))
                clients[client].sendall(str.encode(response))

        if not clientData:
            break
    #finally close the connection
    clientSocket.close()

#MAIN FUNCTION
if __name__ == '__main__':
    #create new server scoket
    serverSocket = socket.socket()
    # declare host name
    host = '127.0.0.1'
    # declare port id
    port = 8000
    processId = 0
    print("Welcome to Vector Clock Simulation Program")
    try:#bind the server
        serverSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print('Distributed Server is waiting for new connections...')
    #listen for incoming messages
    serverSocket.listen(5)

    #loop to handle incoming connections
    while True:
        clientSocket, address = serverSocket.accept()
        #print the client address
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        processId += 1
        #start new thread for client
        start_new_thread(handle_client, (clientSocket, processId, ))
        #store the connection in clients dictionary
        clients[processId] = clientSocket
        print('Process ' + str(processId) + " has connected to server...")
    serverSocket.close()