import threading
import socket

# localhost
host_address = '127.0.0.1'
port_number = 55656

# AF_INET = Internet Socket
# SOCK_STREAM = TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host_address, port_number))
server.listen()

# Lists for holding clients and their usernames
clients = []
usernames = []


# Announce messages to all the clients at once
def announce(message):
    for client in clients:
        client.send(message)


# Try to receive messages from individual clients
def handle(client):
    while True:
        # If possible announce the message to everyone on the chatroom
        try:
            message = client.recv(1024)
            announce(message)
        # If not possible (exception thrown) then cut the connection and broadcast that the user has left
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            announce((str(username) + " left the chat!").encode('ascii'))
            usernames.remove(username)
            break


# Accept connections from clients to the server
def receive():
    while True:
        client, address = server.accept()
        print("Connected to " + str(address))

        # Get the username from the client and store it
        client.send("USERNAME".encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        # Announce the username of the client who has just joined the chatroom to everyone
        print("Username of the client is " + str(username))
        announce((str(username) + " joined the chatroom").encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        # Handle multiple client requests at the same time by using threads simultaneously
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is up and running...")
receive()
