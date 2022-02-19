import socket
import threading
import ssl

# Same host address and the port number which were declared in the server
host_address = '127.0.0.1'
port_number = 55656
server_sni_hostname = 'example.com'
server_cert = 'resources/server.crt'
client_cert = 'resources/client.crt'
client_key = 'resources/client.key'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

# AF_INET = Internet Socket
# SOCK_STREAM = TCP protocol
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = context.wrap_socket(client_socket, server_side=False, server_hostname=server_sni_hostname)
client.connect((host_address, port_number))

username = input("Choose a username: ")


# Receive messages from the server
def receive():
    while True:
        # Check if it's a message or an initial username input
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'USERNAME':
                client.send(username.encode('ascii'))
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
        message = str(username) + ": " + str(input(""))
        # message = str(input(""))
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
