from dnsserver import DnsServer
from constants import PRIMARY_SERVER, SECONDARY_SERVER
from time import sleep
from sys import argv


def main(): 
    
    server = DnsServer(upstream = (SECONDARY_SERVER if argv[-1] == "--secondary" else PRIMARY_SERVER))
    
    server.start()
    
    try:
        while server.is_running:
            sleep(0.001)
    except KeyboardInterrupt:
        pass
    finally:
        print('stopping DNS server')
        server.stop()
     
    server.stop()

if __name__ == "__main__":
    main()