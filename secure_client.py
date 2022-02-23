import socket
import threading
import ssl

# Same host address and the port number which were declared in the server
import time

import login_handler

host_address = '127.0.0.1'
port_number = 55656
server_hostname = 'example.com'

# ssl certificates and rsa key
server_cert = 'resources/server.crt'
client_cert = 'resources/client.crt'
client_key = 'resources/client.key'


context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

# AF_INET = Internet Socket
# SOCK_STREAM = TCP protocol
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# wrapping sockets using ssl socket objects
client = context.wrap_socket(client_socket, server_side=False, server_hostname=server_hostname)
client.connect((host_address, port_number))

# using the login menu handler to ge the initial inputs
user_input = login_handler.handle_login_menu_input()
username = user_input[0]
password = user_input[1]
login_or_register = user_input[2]


stop_thread = False


# Receive messages from the server
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break

        # Login/Registration client side process
        try:
            message = client.recv(1024).decode('ascii')
            if message == "LOGIN_REGISTER":
                client.send(login_or_register.encode('ascii'))
                message = client.recv(1024).decode('ascii')
                if message == "USERNAME":
                    client.send(username.encode('ascii'))
                    message = client.recv(1024).decode('ascii')
                    if message == "PASS":
                        client.send(password.encode('ascii'))
                        message = client.recv(1024).decode('ascii')
                        if message == "REFUSE":
                            print("Connection was refused! Wrong password!")
                            stop_thread = True
                        elif message == "REG_ERROR":
                            print("Connection was refused! Username already taken!")
                            stop_thread = True
            else:
                print(message)

        # Close connection if any errors occurred
        except:
            print("An error occurred")
            client.close()
            break


# Accepting inputs from user constantly
def write():
    while True:
        if stop_thread:
            break

        message = str(username) + ": " + str(input(""))

        # handling admin functionalities
        if message[len(username) + 2:].startswith('/'):
            if username == 'admin':
                if message[len(username) + 2:].startswith('/kick'):
                    client.send(("KICK " + message[len(username) + 2 + 6:]).encode('ascii'))
                elif message[len(username) + 2:].startswith('/ban'):
                    client.send(("BAN " + message[len(username) + 2 + 5:]).encode('ascii'))
                elif message[len(username) + 2:].startswith('/user_list'):
                    client.send("USERS".encode('ascii'))
                elif message[len(username) + 2:].startswith('/warn'):
                    client.send(("WARN " + message[len(username) + 2 + 6:]).encode('ascii'))
            else:
                print("Commands can only be executed by the admin")
        else:
            client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
