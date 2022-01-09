import socket
import json
from dh_processor import *

public_key_1 = 23
public_key_2 = 9
client_private_key = 4

def Main():
    # setting up connection properties
    client_socket = socket.socket()
    host = '127.0.0.1'
    port = 65432
    print("Attempting to establish connection with server....")

    try:
        client_socket.connect((host, port))
        client_socket.settimeout(5)   # 5 seconds
        print("Connection with server: OK")
        Response = client_socket.recv(1024)
        print("1 - Create new user")
        print("2 - Authenticate and send encrypted message")

        selection = input("Select operation to do: ")
        if(selection == "1"):
            create_user(client_socket)
        else:
            send_message(client_socket)
        while True:
            pass
    except socket.error as e:
        print("Connection with server: Failed")
        print ("Caught exception socket.error : %s" % e)

    
        
def create_user(s):
    username = input("Please insert username: ")
    password = input("Please insert password: ")
    confirm_password = input("Please type again password: ")

    if(username == "" and password == "" and password == confirm_password ):
        print("Could not process credentials")
    else:
        data = {
            "menu_selection": "1",
            "username": username,
            "password": password
        }   
        s.send(str.encode(json.dumps(data)))

def send_message(client_socket):
    authenticate(client_socket)
    while True:
        generated_key = generate_key(public_key_2, client_private_key, public_key_1)
        client_socket.send(str.encode(str(generated_key)))
        server_generated_key = client_socket.recv(1024).decode('utf-8');
        client_symmetric_key = generate_key(int(server_generated_key), client_private_key, public_key_1)
        message = input('Type message: ')
        client_socket.send(str.encode(encrypt_message(message, client_symmetric_key)))
        response = client_socket.recv(1024)
        m = decrypt_message(str(response.decode('utf-8')), client_symmetric_key)
        print(m)

def authenticate(s):
    username = input("Please insert username: ")
    password = input("Please insert password: ")
    request_data = {"menu_selection": "2","username": username,"password": password}   
    s.sendall(json.dumps(request_data).encode('utf-8'))


if __name__ == '__main__':
    Main()
