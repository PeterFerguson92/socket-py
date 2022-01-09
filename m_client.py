import socket
import pickle
from dh_processor import *
import sys

public_key_1 = 23
public_key_2 = 9
client_private_key = 4

import sys

def Main():
    # setting up connection properties
    client_socket = socket.socket()
    host = '127.0.0.1'
    port = 65432
    print("Attempting to establish connection with server....")

    try:
        client_socket.connect((host, port))
        client_socket.settimeout(30)   # 5 seconds
        print("Connection with server: OK")
        print("1 - List messages")
        print("2 - Send encrypted message")
        selection = input("Select operation to do: ")
        if(selection == "1"):
            list_messages(client_socket)
        else:
            send_message(client_socket)
    except socket.error as e:
        print("Connection with server: Failed")
        print ("Caught exception socket.error : %s" % e)

    
        
def list_messages(client_socket):
    while True:
        client_symmetric_key = get_ecrypted_key(client_socket)
        message = "list_messages"
        client_socket.send(str.encode(encrypt_message(message, client_symmetric_key)))
        response = client_socket.recv(4096)
        data_arr = pickle.loads(response)
        for myItem in data_arr:
            print(myItem[0])
        response = client_socket.recv(1024)
        m = decrypt_message(str(response.decode('utf-8')), client_symmetric_key)
        print(m)
   
def send_message(client_socket):
    while True:
        client_symmetric_key = get_ecrypted_key(client_socket)
        message = input('Type message: ')
        if(len(message) > 3):
            client_socket.send(str.encode(encrypt_message(message, client_symmetric_key)))
            response = client_socket.recv(1024)
            m = decrypt_message(str(response.decode('utf-8')), client_symmetric_key)
        else:
            print("at least 3 characters")
            sys.exit()


def get_ecrypted_key(client_socket):
    generated_key = generate_key(public_key_2, client_private_key, public_key_1)
    print(generated_key)
    client_socket.send(str.encode(str(generated_key)))
    server_generated_key = client_socket.recv(1024).decode('utf-8')
    return generate_key(int(server_generated_key), client_private_key, public_key_1)

if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
        print ("Interrupted")
        sys.exit(0)
