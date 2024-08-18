from time import sleep
from .server.dnsserver import DnsServer
from .records.record import Record
from .sync.records import fetch_records, save_records


def main():

    server = DnsServer()

    fetch_records()

    server.start()

    try:
        while server.is_running:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("saving records")
        save_records()
        print("stopping DNS server")
        server.stop()


if __name__ == "__main__":
    main()
