import sys
import socket
import pickle
from _thread import *
import threading
import os
import random

def swagata(conn, addr, port, buffsize) :
        
    # Recieve the chain info and URL from connection
    data = conn.recv(buffsize)
    # 2d array with each array being a connection in the chaingang.txt, with the last array being one element (the URL)
    data_arr = pickle.loads(data)
    ss_arr = data_arr[:]
    ss_arr.remove(ss_arr[len(ss_arr)-1])
    
    # Grabbing the filename of what was sent (the last element after the last forward slash)
    if('/' in data_arr[len(data_arr) - 1]):
        filename = data_arr[len(data_arr) - 1].split('/').pop()
    # If no file name is specified, this is the default
    else:
        filename = "index.html"
        
    print("Request: " + data_arr[len(data_arr) - 1] + "...")
    if len(ss_arr) == 0 : 
        print("chainlist is empty")
        print("issuing wget for file " + str(filename))
    else :
        print("chainlist is ")
        print(*ss_arr, sep = "\n")
    
    # Checks if the chainlist is empty AKA only the URL remains in the data_arr
    if len(data_arr) == 1:
            
        # Executing wget() System call
        command = "wget " + data_arr[0]
        os.system(command)
        print("File recieved")
        print("Relaying file ...")
        
        # Read the file in small chunks to transmit previous ss
        send_read_file(conn, filename, buffsize)
            
    # If there are still ss's in the chaingang.txt
    else :
        randomChoice = random.choice(ss_arr)
        print("next SS is " + str(randomChoice))
        data_arr.remove(randomChoice)
        nextss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nextss.connect((randomChoice[0],int(randomChoice[1])))
        nextss.send(pickle.dumps(data_arr))
        print("waiting for file ...")
        recievingFile(nextss, filename)
        print("Relaying file...")
        send_read_file(conn, filename, buffsize)
        
    # Delete local file
    ######### NEED TO CHANGE FOR CS MACHINES #########
    command2 = "rm "+ filename
    os.system(command2)
    ######### NEED TO CHANGE FOR CS MACHINES ######### change to os.system(command)
    print("Goodbye!")
        

def send_read_file(socket, filename, buffsize) :
    f = open(filename,'rb')
    while True:
        l = f.read(buffsize)
        while (l):
            socket.send(l)
            l = f.read(buffsize)
            if not l:
                f.close()
                socket.close()
                break
        break

def recievingFile(sock, filename):
    with open(filename, 'wb') as f:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            f.write(data)

def ss(chaingang=None, port=None) :
    # Variable Setup
    buffsize = 1024
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    
    # Print name of host ss is running on
    
    # Determine if a port number was passed via system arguments
    if port == None :
        port = 20000
        
    # Create Socket and bind it to given port and ip it's running on
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssSocket.bind((ip, int(port)))
        
    # Listen for a connection
    ssSocket.listen(1)
        
    # Loop statement to do stuff
    while True :
        # Accept the connection
        conn, addr = ssSocket.accept()
        
        # Start a new thread with the ss() function and the data_arr arguments
        t = threading.Thread(target=swagata, args=(conn, addr, port, buffsize, ), daemon=False)
        t.start()
            
    ssSocket.close()

def main() :
    if len(sys.argv) == 2 :
        ss(None, sys.argv[1])
    else :
        ss()

if __name__ == "__main__" :
    main()
