import socket  # Import socket module
import json # Import json module
from dh_processor import *
message="This is a very secret message!!!"
public_key_1 = 23
public_key_2 = 9
client_private_key = 4

def Main():
    # setting up connection properties
    host = '127.0.0.1'
    port = 65432
    ThreadCount = 0


    try:
        # open connection with the setting above
        s = socket.socket()
        print("Attempting to establish connection with server....")
        s.connect((host, port))
        s.settimeout(5)   # 5 seconds
        print("Connection with server: OK")

        generated_key = generate_key(public_key_2, client_private_key, public_key_1)
        s.send(str(generated_key).encode())
        server_generated_key = s.recv(1024).decode('utf-8');
        client_symmetric_key = generate_key(int(server_generated_key), client_private_key, public_key_1)
        print("Select one")
        print("1 - create new user")
        print("2 - Process Cvs")

        menu_selection = input("Select operation to do: ")
        if(menu_selection == "1"):
            create_user(s)
        else:
            process_file(s, client_symmetric_key)
        # input of the csv file name to process(hard-coded or by user input)
        # Filename = 'csv.txt'
        
    except socket.error as exc:
        print("Connection with server: Failed")
        print ("Caught exception socket.error : %s" % exc)

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

def authenticate(s):
    username = input("Please insert username: ")
    password = input("Please insert password: ")
    request_data = {"menu_selection": "2","username": username,"password": password}   
    s.sendall(json.dumps(request_data).encode('utf-8'))

def process_file(s, key):
    authenticate(s)
    data = s.recv(1024).decode('utf-8') 
    if(data == "1"):
        request_data = {"menu_selection": "0","message": encrypt_message(message, key)}   
        s.sendall(json.dumps(request_data).encode('utf-8'))
    else:
        print("Login failed")
    
    

    # file_name = input("Name of file to process: ")
    # s.send(file_name.encode('utf-8'))
    # s.shutdown(socket.SHUT_WR) 
    # data = s.recv(1024).decode('utf-8') 

    # try:
    #     # received the data in string format, 
    #     # so need to convert in a dict/json to easily read the result
    #     json_acceptable_string = data.replace("'", "\"") 
    #     result = json.loads(json_acceptable_string)

    #     # printing of the result on screen
    #     print('How many people in the list are male?  ' + str(result['males']))
    #     print('How many people in the list are older than 30?  ' + str(result['above_threshold']))
    #     print('How many employers are in Human Resources? ' + str(result['hr']))

    #     # closing of the connection
    #     s.close()
    # except Exception:
    #     print("Could not process your request, please see the server logs")


if __name__ == '__main__':
    Main()

