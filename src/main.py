from dnserver import DNSServer
from time import sleep
from sys import argv

PRIMARY_SERVER = "208.67.222.222"
SECONDARY_SERVER = "208.67.220.220"


def main(): 
    
    server = DNSServer(upstream = (SECONDARY_SERVER if argv[-1] == "--secondary" else PRIMARY_SERVER))
    
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