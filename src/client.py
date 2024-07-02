from socket import socket
from g import *

def main():

    for _ in range(RANGE):
        s = socket()
        
        s.connect(('127.0.0.1', PORT))
        
        print(s.recv(1024))
        
        s.close()
    

if __name__ == "__main__":
    main()