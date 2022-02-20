import threading
import socket
import ssl

# localhost
host_address = '127.0.0.1'
port_number = 55656

# ssl certificates and rsa key
server_cert = 'resources/server.crt'
server_key = 'resources/server.key'
client_cert = 'resources/client.crt'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_cert)

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
        client_socket, address = server.accept()
        print("Connected to " + str(address))

        # wrapping sockets using ssl socket objects
        client = context.wrap_socket(client_socket, server_side=True)

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
