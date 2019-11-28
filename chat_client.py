import socket
import select
import errno
import sys

data_length = 10
ip = "127.0.0.1"
port = 1234
my_username = input("Username: ")
#Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Given ip and port to connect to
client_socket.connect((ip, port))
#Wont block rec data
client_socket.setblocking(False)
#Set a username
username = my_username.encode('utf-8')
username_header = f"{len(username):<{data_length}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    #Input a message to send to server
    message = input(f"{my_username} > ")
    #If user types a message it will encode it and send it to the server
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {data_length}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        #Now to receive message from other users
        while True:
            #Receive user length
            username_header = client_socket.recv(data_length)
            #If no data is received disconnect from server
            if not len(username_header):
                print("Conn closed by server")
                sys.exit()
            #User lenght is converted to an int
            username_length = int(username_header.decode('utf-8').strip())
            #Username is received and decoded
            username = client_socket.recv(username_length).decode('utf-8')
            #Do the same to the message received
            message_header = client_socket.recv(data_length)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            #Print the message
            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reader error", str(e))        
            sys.exit()
        continue

    except Exception as e:
        print('Error'.format(str(e)))
        sys.exit()