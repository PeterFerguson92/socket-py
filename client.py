import socket  # Import socket module
import json # Import json module

def Main():
    # setting up connection properties
    host = '127.0.0.1'
    port = 65432

    try:
        # open connection with the setting above
        s = socket.socket()
        print("Attempting to establish connection with server....")
        s.connect((host, port))
        s.settimeout(5)   # 5 seconds
        print("Connection with server: OK")

        print("Select one")
        print("1 - create new user")
        print("2 - Process Cvs")

        menu_selection = input("Select operation to do: ")
        if(menu_selection == "1"):
            create_user(s)
        else:
            process_file(s)
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

    request_data = {
            "menu_selection": "2",
            "username": username,
            "password": password
        }   
    s.send(str.encode(json.dumps(request_data)))

def process_file(s):
    authenticate(s)
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

