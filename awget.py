import sys
import os.path
import random
import socket
import pickle

#reading the chain file and extracting the URL
def readFile():
    filename = ""
    if(len(sys.argv)<2):
        print("Please enter URL and entering the chain file if optional")
        exit(1)
    else:
        filename = "chaingang.txt"
        URL = sys.argv[1]
        if(len(sys.argv)==3):
            filename = sys.argv[2]
    return filename,URL

#getting the random SS from the chainfile
def getSS(filename):
    try:
        f = open(filename)
        lenght = f.readline()
        ss=[]
        for x in range(0, int(lenght)):
            ss.append(f.readline().split())
        f.close()
        randomChoice = random.choice(ss)
        return randomChoice, ss
    except FileNotFoundError:
        print('File does not exist')

#code for receiving the file through the different hops and saving it        
def recievingFile(sock,URL):
    url_filename="index_recieved.html"
    if('/' in URL):
        url_filename = URL.split('/').pop()
        
    with open(url_filename, 'wb') as f:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            f.write(data)
    print("Receive file "+url_filename)
    print("Goodbye!")
    
#starting a connection with the random SS and waiting to receive    
def start_connection(choice,ss,URL):
    addr = (choice[0], int(choice[1]))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.remove(choice)
    ss.append(URL)
    data_string = pickle.dumps(ss)
    sock.connect(addr)
    print(choice)
    sock.send(data_string)
    recievingFile(sock,URL)

filename, URL = readFile()
choice,ss = getSS(filename)
print("awget:")
print("Request: ",URL)
print("chainlist is")
for i in ss:
    print(str(i))
print("next SS is "+str(choice))
print("waiting for file...")
print("...")
start_connection(choice,ss,URL)