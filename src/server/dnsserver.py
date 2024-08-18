from __future__ import annotations as _annotations

from dnslib.server import DNSServer as LibDNSServer
from src.local.record import Record
from src.server.proxy_resolver import ProxyResolver
from src.local.zone import Zone, RecordType

DEFAULT_PORT = 53
LEVELS = ["high", "low"]
OPENDNS_UPSTREAMS = ["208.67.222.222", "208.67.220.220"]
MAFAZAA_UPSTREAMS = ["15.184.191.201", "15.184.243.155"]


class DnsServer:
    def __init__(self) -> None:
        self.upstream = self.choose(MAFAZAA_UPSTREAMS, "proxy server upstream: ")
        self.level = self.choose(LEVELS, "protection level: ")
        self.udp_server: LibDNSServer | None = None
        self.tcp_server: LibDNSServer | None = None
        self.records = Record.fetch_records()

    def start(self):
        print(
            f'starting DNS server on port {DEFAULT_PORT}, upstream DNS server "{self.upstream}"'
        )
        resolver = ProxyResolver(self.upstream)

        self.udp_server = LibDNSServer(resolver, port=DEFAULT_PORT)
        self.tcp_server = LibDNSServer(resolver, port=DEFAULT_PORT, tcp=True)

        self.udp_server.start_thread()
        self.tcp_server.start_thread()

    def stop(self):
        self.udp_server.stop()
        self.udp_server.server.server_close()
        self.tcp_server.stop()
        self.tcp_server.server.server_close()

    @property
    def is_running(self):
        return (self.udp_server and self.udp_server.isAlive()) or (
            self.tcp_server and self.tcp_server.isAlive()
        )

    def choose(self, options, prompt):
        length = len(options)
        print(prompt, end="\n\n")
        for i, x in enumerate(options):
            print(f"({i}) {x}")
        while True:
            value = int(input("answer: "))
            if value > length:
                continue
            return options[value]
