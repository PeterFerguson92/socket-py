#!/usr/bin/env python3
import socket
import json
import hashlib
import sqlite3

# import processor function
from csv_processor import process
from dh_processor import *

general_error_message = 'File not found. Check the file name and try again.'
file_not_found_error_message = 'Something went wrong while processing, please check the format and content of file'
connection_error_message = 'Could not start up server, please contact the technical team'
message = 'Python is fun'

# convert string to bytes
byte_message = bytes(message, 'utf-8')
public_key_1 = 23
public_key_2 = 9
server_private_key = 3

def Main():

    db_connection = sqlite3.connect('shows.db')
    cursor = db_connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    # connection settings
    host = '127.0.0.1'
    port = 65432

    try: 
        #connection startup with the settings above
        s = socket.socket()
        print("Starting up server")
        s.bind((host,port))
        print("Server Running...")
        s.listen(5)
        c, addr = s.accept()
        print("Connection from: " + str(addr))
        
        generated_key = generate_key(public_key_2, server_private_key, public_key_1)
        client_generated_key = c.recv(1024).decode('utf-8');
        c.send(str(generated_key).encode())
        server_symmetric_key = generate_key(int(client_generated_key), server_private_key, public_key_1)

        # This loop accepts a connection, then reads from the 
        # client until done
        while True:
            data = c.recv(1024).decode('utf-8')
            print(data)
            if not data:
                break
            else: 
                payload = json.loads(data) 
                print(payload)
                menu_selection = str(payload['menu_selection'])
                print(menu_selection)
                if(menu_selection == "0"):
                    m = decrypt_message(str(payload['message']), server_symmetric_key)
                    print(m)
                else:
                    username = str(payload['username'])
                    password = str(payload['password'])
                if(menu_selection == "1"):    
                    create_user(db_connection, cursor, username, password)
                if(menu_selection == "2"):
                    result = authenticate_user(cursor, username, password)
                    c.send(result.encode())

    except socket.error:
        # connection error handling 
        print(connection_error_message)
        c.send(file_not_found_error_message.encode())
        c.close()

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()        


def create_user(db_connection, cursor, username, password):    
    rows = get_user_by_username(cursor, username)   
    if(len(rows) > 0):
        print("user already exists")
    else:    
        hashed_password = hash_pw(password) 
        cursor.execute('''INSERT INTO users (username, password) VALUES(?,?)''', (username, hashed_password))
        db_connection.commit()
        print("user created successfully")

def authenticate_user(cursor, username, password):     
    users = get_user_by_username(cursor, username)
    if(len(users) == 0):
        print("user already exists")
    else:
        user = users[0]    
        user_password = user[1]
        if(user_password == hash_pw(password)):
            print("user logged successfully")
            return "1"
        else:
            print("user logged failed") 
            return "-1"

def get_user_by_username(cursor, username):
    cursor.execute("SELECT * FROM users WHERE username=?", [username])
    return cursor.fetchall()

def hash_pw(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), byte_message ,100000, dklen=128) 

def process_file(c):
    filename = ''
    # This loops keeps the server running until an EOF 
    # (we've receive zero length string in python socket), this should happen
     # when the client socket has been shutdown
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        filename += data
        print("File to process: " + filename)

        # open the csv file in read mode (we could open in binary mode with 'rb' but to make
        # the processing of the file we are opening it in read mode)
        try:
            myfile = open(filename, "r")
            try:
                # call to the process function in the csv_processor.py file
                result = process(myfile)

                # encoding the result in a binary object using the json library in order to send the data
                # back the client in bytes-like object format
                encoded_result = json.dumps(result, indent=2).encode('utf-8')
                c.send(encoded_result)
                # closing of the connection
                c.close()
            except Exception:
                # file processing error handling
                print(general_error_message)
                c.send(general_error_message.encode()) 
                c.close
        except OSError as os:
            print(os)
            # file not found error handling
            print (file_not_found_error_message)
            c.send(file_not_found_error_message.encode())
            c.close


if __name__ == '__main__':
    Main()