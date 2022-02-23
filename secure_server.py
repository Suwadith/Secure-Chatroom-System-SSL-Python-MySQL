import threading
import socket
import ssl

# localhost
import time

import database_handler
import log_writer

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

        try:
            msg = message = client.recv(1024)

            # handling kick request from admin
            if msg.decode('ascii').startswith('KICK'):
                if usernames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))

            # handling ban request from admin
            elif msg.decode('ascii').startswith('BAN'):
                if usernames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    ban_user(name_to_ban, client)
                    kick_user(name_to_ban)
                    # print(name_to_ban + "has been banned!")
                else:
                    client.send('Command was refused!'.encode('ascii'))

            # handling warning request from admin
            elif msg.decode('ascii').startswith('WARN'):
                if usernames[clients.index(client)] == 'admin':
                    username = msg.decode('ascii')[5:]
                    name_index = usernames.index(username)
                    client = clients[name_index]
                    client.send('You have been warned by the admin!!!!'.encode('ascii'))
                else:
                    client.send('Command was refused!'.encode('ascii'))

            # printing active user list
            elif msg.decode('ascii').startswith('USERS'):
                for username in usernames:
                    client.send(username.encode('ascii'))

            else:
                # announce the message to everyone on the chatroom
                announce(message)

                # store public chat into the database
                database_handler.store_public_chat(msg.decode('ascii').split(": ")[0], msg.decode('ascii').split(": ")[1])

        # If not possible (exception thrown) then cut the connection and broadcast that the user has left
        # Basically an automatic logout operation
        except:
            if client in clients:
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
        log_writer.write_to_log("Connected to " + str(address))

        # wrapping sockets using ssl socket objects
        client = context.wrap_socket(client_socket, server_side=True)

        # Get the option to login/register from the client and store it
        client.send("LOGIN_REGISTER".encode('ascii'))
        login_or_register = client.recv(1024).decode('ascii')

        # Get the username from the client and store it
        client.send("USERNAME".encode('ascii'))
        username = client.recv(1024).decode('ascii')

        # Get the password from the client and store it
        client.send("PASS".encode('ascii'))
        password = client.recv(1024).decode('ascii')

        # Handling login or registration process on the serverside
        if login_or_register == '1':
            result = database_handler.check_password(username, password)
            if result:
                usernames.append(username)
                clients.append(client)
            else:
                client.send("REFUSE".encode('ascii'))
                client.close()
                continue
        elif login_or_register == '2':
            result = database_handler.register_user(username, password, 'user')
            if result:
                usernames.append(username)
                clients.append(client)
            else:
                client.send("REG_ERROR".encode('ascii'))
                client.close()
                continue

        # checking if the username has already been added in the DB ban list
        username_ban_check = database_handler.check_username_banned(username)
        # checking if the username has already been added in the DB ban list
        ip_ban_check = database_handler.check_ip_banned(client.getpeername()[0])

        # if IP and username are same then the user gets kicked
        # (Using an 'or' condition will make both the IP and the username banned)
        if username_ban_check and ip_ban_check:
            kick_user(username)

        # Announce the username of the client who has just joined the chatroom to everyone
        print("Username of the client is " + str(username))

        # log server messages into a txt file
        log_writer.write_to_log("Username of the client is " + str(username))
        announce((str(username) + " joined the chatroom").encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        # Handle multiple client requests at the same time by using threads simultaneously
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# method to handle kicking users
def kick_user(username):
    if username in usernames:
        name_index = usernames.index(username)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send("You have been kicked by the admin!".encode('ascii'))
        usernames.remove(username)
        client_to_kick.close()
        announce((username + " was kicked by the admin!").encode('ascii'))
        print(username + " was kicked by the admin!")
        log_writer.write_to_log(username + " was kicked by the admin!")


# method to handle banning users by obtaining both username and ip address
def ban_user(username, client):
    database_handler.ban_user(username, client.getpeername()[0])
    announce((username + ", " + client.getpeername()[0] + " was banned by the admin!").encode('ascii'))
    print(username + ", " + client.getpeername()[0] + " was banned by the admin!")
    log_writer.write_to_log(username + ", " + client.getpeername()[0] + " was banned by the admin!")


print("Server is up and running...")
log_writer.write_to_log("Server is up and running...")
receive()
