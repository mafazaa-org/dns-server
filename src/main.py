from dnserver import DNSServer
from time import sleep
from argparse import ArgumentParser



def main(): 
    
    args = parse_args()
    
    server = DNSServer(upstream=args.secondary)
    
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

def parse_args():
    parser = ArgumentParser("DNS Server", "dns [--secondry]", description="An upstream dns server")
    parser.add_argument("--secondary", "-s", help="", nargs="?", default="208.67.222.222", const="208.67.220.220")
        
    return parser.parse_args()

if __name__ == "__main__":
    main()