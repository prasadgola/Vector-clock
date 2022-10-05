import socket
from _thread import *

# global clock to hold the process events
vector_clock = {}

# function to print the current state of clocks
def print_clocks():
    result = "["
    #iterate the vector clock
    for item in vector_clock:
        # append the event id to result
        result = result + vector_clock[item] + " "
    result=result + "]"
    #print the result
    print(result)

#function to update the clocks
def update_clocks(clocks):
    #update the source process event
    vector_clock[clocks[0]] = clocks[2]
    # update the destination process event
    vector_clock[clocks[1]] = clocks[3]

#function to handle the incoming messages for the client process
def receiver_thread(client):
    # start infinite loop
    while True:
        #receive message from server
        msg = client.recv(2048)
        #decode the message from bytes to string
        msg = msg.decode('utf-8')
        #split the message using semi colon for getting the type and actual event
        result = msg.split(":")
        #get message type
        type = str(result[0])
        print(result)
        #get event message
        clocks = str(result[1]).split(",")
        #if its personal message then print previous state and update the vectors
        # and finally print the updated state
        if type == "p":
            print("-----------------------------------")
            print("Process " + str(clocks[0]) + " has sent an event " + str(result[1]))
            print("Before update")
            print_clocks()
            update_clocks(clocks)
            print("After update")
            print_clocks()
            print("-----------------------------------")
        else: # for broadcast message simply update the clocks
            print("updating clocks...")
            update_clocks(clocks)

#MAIN FUNCTION to handle to client programming
if __name__ == '__main__':
    #declare client socket
    clientSocket = socket.socket()
    #declare host name
    host = '127.0.0.1'
    #declare port id same as server
    port = 8000
    #print welcome messages and instructions
    print("---------------------------------------------")
    print('Welcome to Vector clock simulation program')
    print("---------------------------------------------")
    print("Instructions to send event message")
    print("Message format : destination_id, source_event, destination_event")
    print("For example: 2,2,1")
    #connect to server
    try:
        clientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))
    #receive generated client id from server
    msg = clientSocket.recv(1024)
    #decode the message
    clientId = msg.decode('utf-8')
    print("Connecting to distributed server as new client with id " + str(clientId))
    #create new receiver thread for the client
    start_new_thread(receiver_thread, (clientSocket,))
    #open infinite loop for sending messages to other clients through server
    while True:
        #prompt the user to enter event
        event = input('Enter event message: ')
        msg = str(clientId)+","+event
        #decode and send the event to server
        clientSocket.send(str.encode(msg))
    #close connection
    clientSocket.close()