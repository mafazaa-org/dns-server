from .server.dnsserver import DnsServer
from .records.block import Block
from .records.zone import Zone


def main():

    server = DnsServer()

    Zone.initialize()
    Block.initialize()

    server.start()

    server.serve_forever()


if __name__ == "__main__":
    main()
