CSV IMPORTER

This project consists in a csv importer, the client application accepts in input the name of the csv file and sends it to the server which elaborates the data to retrieve some information and prints it out:

INFORMATION RETRIEVED:
The information retrieved by this application are the answers to the following questions:

1. How many people in the list are male?
2. How many people in the list are older than 30?
3. How many employers are in Human Resources?


HOW TO RUN IT:
-Linux/Mac machine: 
    open one tab in terminal and run this command: python3 client.py
    open second tab in terminal and run this command: python3 server.py

-Windows Machine:
    open one tab in terminal and run this command: python3 client.py
    open second tab in terminal and run this command: python3 server.py


HOW IT WORKS
Once the client and server are running, the client application will prompt the user to
input the name of the file to process. 
The name of the file will be sent to the server application which will try and open the file (it needs to be in the same folder of the server.py script).

    - If the file is found and it's a valid csv file with the right header, it will process the data    row by row and return to the client the result.

    -If the file is not found or is the format is not valid it will throw an error

If the client do not get a response by a certain interval by the server it will exit (at the moment is defaulted to 5 seconds).  

SETUP DATA

In the folder, aside from the project scripts some setup data can be found, this files are used to test the most commons scenarios for the application and they have the following properties and expected results:

    - test.csv -- small sample of data -- the application should process ok this file
    - test2.csv -- big sample of data -- the application should NOT be able to process this file     since the age column is missing
    - test3.csv --  big sample of data -- the application should be able to process this file
    -csv.txt -- empy file -- the application should NOT be able to process this file since is not a valid csv file but rather a txt.file.