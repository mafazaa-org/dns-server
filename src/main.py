from dnserver import DNSServer
from time import sleep

def main(): 
    
    server = DNSServer.from_toml( zones_file="src/zones.toml", upstream = "Server")
    
    server.start()
    
    try:
        while server.is_running:
            sleep(0.001)
    except KeyboardInterrupt:
        pass
    finally:
        print('stopping DNS server')
        server.stop()
     
if __name__ == "__main__":
    main()