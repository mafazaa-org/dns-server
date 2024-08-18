from __future__ import annotations as _annotations

from dnslib.server import DNSServer as LibDNSServer
from src.server.proxy_resolver import ProxyResolver
from src.utils.choose import choose
from os import environ

DEFAULT_PORT = 53
UPSTREAMS = ["208.67.222.222", "208.67.220.220"]


class DnsServer:
    def __init__(self) -> None:
        self.upstream = choose(UPSTREAMS, environ["server"], ["primary", "secondary"])
        self.udp_server: LibDNSServer | None = None
        self.tcp_server: LibDNSServer | None = None

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
