from __future__ import annotations as _annotations

from time import sleep
from dnslib.server import DNSServer as LibDNSServer
from src.server.proxy_resolver import ProxyResolver
from src.constants import DEFAULT_PORT


class DnsServer:
    def __init__(self) -> None:
        self.udp_server: LibDNSServer | None = None
        self.tcp_server: LibDNSServer | None = None

    def start(self):
        print(f"starting DNS server on port {DEFAULT_PORT}")
        resolver = ProxyResolver()

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

    def serve_forever(self):
        try:
            while self.is_running:
                sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            print("stopping DNS server")
            self.stop()
