import socket
import select
from threading import Thread

data_length = 10
ip = "127.0.0.1"
port = 1234

#Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Tells socket it will be provided with ip and port
server_socket.bind((ip, port))

#Socket server listening for connection
server_socket.listen()

#List of sockets includes server from beginning
sockets_list = [server_socket]

#List of clients connected
clients = {}

#Can tell server is listening
print(f'Listening for connections on {ip}:{port}:')

#Takes care of messages received by server
def rec_msg(client_socket):
    try:
        #Length of message defined
        msg_data = client_socket.recv(data_length)
        #If server do not receive any message (data) connection is closed
        if not len(msg_data):
            return False
        #Length of message is defined by an int
        msg_length = int(msg_data.decode('utf-8').strip())
        #Return message lenght and message data
        return {'header':msg_data, 'data':client_socket.recv(msg_length)}
    except:
        #Crashes and so on closes the connection
        return False

def Main():
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [],sockets_list)
        for notified_socket in read_sockets:
            #If notified socket is a new connection accept it
            if notified_socket == server_socket:
                #Accept new socket, unique for that client
                client_socket, client_address = server_socket.accept()
                #Receive user name from client
                user = rec_msg(client_socket)
                #If user is False disconnect
                if user is False:
                    continue
                #Accept client socket to client list
                sockets_list.append(client_socket)
                #Save the username 
                clients[client_socket] = user
                print('New connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
            else:
                #Receive message
                message = rec_msg(notified_socket)
                #If no message is sent disconnect client
                if message is False:
                    print("Closed conn from: {}".format(clients[notified_socket]['data'].decode('utf-8')))
                    #Remove client from socket list
                    sockets_list.remove(notified_socket)
                    #Remove client from client list
                    del clients[notified_socket]
                    continue
                #Will see who sent a message
                user = clients[notified_socket]
                print(f"Recv message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
                #Loop all clientsto send message
                for client_socket in clients:
                    #Dont send it to the sender
                    if client_socket != notified_socket:
                        #Send message to all other clients
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

if __name__=="__main__":
    Main()