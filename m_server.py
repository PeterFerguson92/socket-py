import socket
from _thread import *
from dh_processor import *
import sqlite3


server_socket = socket.socket()
host = '127.0.0.1'
port = 65432
ThreadCount = 0

public_key_1 = 23
public_key_2 = 9
server_private_key = 3

db_connection = sqlite3.connect('shows.db')
cursor = db_connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
try:
    server_socket.bind((host, port))
    
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
server_socket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        generated_key = generate_key(public_key_2, server_private_key, public_key_1)
        client_generated_key = connection.recv(2048)
        connection.send(str(generated_key).encode())
        server_symmetric_key = generate_key(int(client_generated_key), server_private_key, public_key_1)
        data = connection.recv(2048)
        decrypt_message(str(data.decode('utf-8')), server_symmetric_key)
        if not data:
            break
        mc = encrypt_message("Server Says: Everything is ok", server_symmetric_key)
        connection.sendall(str.encode(mc))
    connection.close()

while True:
    Client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

