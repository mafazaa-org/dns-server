from .server.dnsserver import DnsServer
from .records.record import Record
from .records.cache import Cache
from .records.block import Block
from dotenv import load_dotenv


def main():
    load_dotenv()

    server = DnsServer()

    Record.initialize()
    Cache.initialize()
    Block.initialize()

    server.start()

    server.serve_forever()


if __name__ == "__main__":
    main()
