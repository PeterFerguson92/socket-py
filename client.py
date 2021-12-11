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

        # input of the csv file name to process(hard-coded or by user input)
        # Filename = 'csv.txt'
        Filename = input("Name of file to process: ")

        s.send(Filename.encode('utf-8'))
        s.shutdown(socket.SHUT_WR) 
        data = s.recv(1024).decode('utf-8') 

        try:
            # received the data in string format, 
            # so need to convert in a dict/json to easily read the result
            json_acceptable_string = data.replace("'", "\"") 
            result = json.loads(json_acceptable_string)

            # printing of the result on screen
            print('How many people in the list are male?  ' + str(result['males']))
            print('How many people in the list are older than 30?  ' + str(result['above_threshold']))
            print('How many employers are in Human Resources? ' + str(result['hr']))

            # closing of the connection
            s.close()
        except Exception:
            print("Could not process your request, please see the server logs")
    except socket.error as exc:
        print("Connection with server: Failed")
        print ("Caught exception socket.error : %s" % exc)

if __name__ == '__main__':
    Main()

