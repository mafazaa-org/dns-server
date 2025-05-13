from .server.dnsserver import DnsServer
from .records.record import Record
from .records.cache import Cache
from .records.block import Block

def main():
    print("starting dns server...")
    server = DnsServer()

    Record.initialize()
    Cache.initialize()
    Block.initialize()

    server.start()

    server.serve_forever()


if __name__ == "__main__":
    main()
