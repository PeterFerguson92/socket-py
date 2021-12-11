#!/usr/bin/env python3
import socket
import json

# import processor function
from csv_processor import process

general_error_message = 'File not found. Check the file name and try again.'
file_not_found_error_message = 'Something went wrong while processing, please check the format and content of file'
connection_error_message = 'Could not start up server, please contact the technical team'

def Main():
    # connection settings
    host = '127.0.0.1'
    port = 65432

    try: 
        #connection startup with the settings above
        s = socket.socket()
        print("Starting up server")
        s.bind((host,port))
        print("Server Running...")
        s.listen(1)

        # This loop accepts a connection, then reads from the 
        # client until done
        while True:
            filename = ''
            c, addr = s.accept()
            print("Connection from: " + str(addr))
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
                    c.close;
            except OSError as os:
                print(os)
                # file not found error handling
                print (file_not_found_error_message)
                c.send(file_not_found_error_message.encode())
                c.close;
    except socket.error:
        # connection error handling 
        print(connection_error_message)
        c.send(file_not_found_error_message.encode())
        c.close;

if __name__ == '__main__':
    Main()