import socket
import threading

# Same host address and the port number which were declared in the server
host_address = '127.0.0.1'
port_number = 55656

# AF_INET = Internet Socket
# SOCK_STREAM = TCP protocol
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host_address, port_number))

username = input("Choose a username: ")
if username == 'admin':
    password = input("Enter password for admin: ")

stop_thread = False

# Receive messages from the server
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        # Check if it's a message or an initial username input
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'USERNAME':
                client.send(username.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Wrong password!")
                        stop_thread = True
                elif next_message == 'BAN':
                    print("Connection refused because of ban!")
                    client.close()
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
        if message[len(username)+2:].startswith('/'):
            if username == 'admin':
                if message[len(username)+2:].startswith('/kick'):
                    client.send(("KICK " + message[len(username)+2+6:]).encode('ascii'))
                    # print(("KICK " + message[len(username)+2+6:]).encode('ascii'))
                elif message[len(username)+2:].startswith('/ban'):
                    client.send(("BAN " + message[len(username)+2+5:]).encode('ascii'))
                # print("in")
            else:
                print("Commands can only be executed by the admin")
        else:
            client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
