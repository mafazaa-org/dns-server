from time import sleep
from dnsserver import DnsServer

def main(): 
    
    server = DnsServer("15.184.191.201")
        
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