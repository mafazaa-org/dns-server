from time import sleep
from .server.dnsserver import DnsServer
from .records.record import Record


def main():

    server = DnsServer()

    server.start()

    try:
        while server.is_running:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("stopping DNS server")
        server.stop()


if __name__ == "__main__":
    main()
