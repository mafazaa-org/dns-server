from socket import socket
from g import *

def main():
    
    s = socket(-1, -1)
    
    s.bind(('', PORT))
    
    s.listen(5)
    
    for i in range(RANGE):
        
        c , adrr = s.accept()
        
        print("Got connection from ", ':'.join([str(x) for x in adrr]))
        
        c.send(b"thank you for connecting")
                
        c.close()
    
if __name__=="__main__":
    main()