from .server.dnsserver import DnsServer
from .records.record import Record
from .records.cache import Cache
from .records.block import Block
from requests import post
from env import DB_ADDR, LEVEL, SERVER_HOSTNAME


def main():

    server = DnsServer()

    post(f"{DB_ADDR}/update/redis?level={LEVEL}&server={SERVER_HOSTNAME}")

    Record.initialize()
    Cache.initialize()
    Block.initialize()

    server.start()

    server.serve_forever()


if __name__ == "__main__":
    main()
