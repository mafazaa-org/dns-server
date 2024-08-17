from time import sleep
from .server.dnsserver import DnsServer

def main(): 
    
    server = DnsServer("157.241.6.180")
        
    server.start()
    
    try:
        while server.is_running:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print('stopping DNS server')
        server.stop()
     
if __name__ == "__main__":
    main()