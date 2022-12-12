# Secure-Chatroom-System-SSL-Python-MySQL

## Software requirements
1. Python 3.4 or above
2. Latest pip version 21.x.x or above preferred


## Setting up the MySQL DB
1. create a user on the db with username='admin' and password='admin' with all the admin/root privileges
2. create a database named 'chatroom'
3. import the resources/chatroom.sql file on to the database
4. make sure the server is up and running and using the default port


## Creating SSL certificates and RSA keys for both the server and client
1. execute the following command to generate server certificate and key
> $ openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt

> NOTE: enter ‘example.com’ for Common Name when asked

2. execute the following command to generate client certificate and key
> $ openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt

> NOTE: enter ‘example.com’ for Common Name when asked (Not really required for client though)
    
3. place them inside the 'resources' folder
> NOTE: You can skip this step as the pre created files have been shared inside the resources folder and they will be picked up by the program automatically


## Setting up the virtual environment and executing the program
1. execute the following command on the root directory(basically inside the code repository) to set up the virtual environment
  > $ python3 -m venv venv
2. execute the below command on the same directory to use or activate the virtual environment
  - Windows
    > $ venv\Scripts\activate
  - Linux
    > $ source venv/bin/activate
3. install the dependencies using the following command using the virtual environment
  > $ pip install -r requirements.txt
4. run the following command to start the server using the virtual environment (You should only run this once as there can only be 1 server listening for incoming connections on the same port)
  > $ python secure_server.py
5. run the following command to start multiple clients using the virtual environment (You can execute this multiple times in different terminals to create multiple client instances)
  > $ python secure_client.py


### Admin commands (username='admin', password='admin')
  1. kick a specific user
  > $ /kick username
  2. warn a particular user
  > $ /warn username
  3. ban a particular user
  > $ /ban username
  4. view active user list
  > $ /user_list
  
  > Note: This program was developed as part of an assessment given by the Middlesex University
