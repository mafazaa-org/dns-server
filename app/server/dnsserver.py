from __future__ import annotations as _annotations

from dnslib.server import DNSServer as LibDNSServer
from app.server.proxy_resolver import ProxyResolver
from app.constants import DEFAULT_PORT
from time import sleep


class DnsServer:
    def __init__(self) -> None:
        self.udp_server: LibDNSServer | None = None
        self.tcp_server: LibDNSServer | None = None

    def start(self):
        resolver = ProxyResolver()

        self.udp_server = LibDNSServer(resolver,"0.0.0.0", port=DEFAULT_PORT)
        self.tcp_server = LibDNSServer(resolver,"0.0.0.0", port=DEFAULT_PORT, tcp=True)

        self.udp_server.start_thread()
        self.tcp_server.start_thread()
        print(f"started DNS server on port {DEFAULT_PORT}")
        

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
            print("stopping DNS server...")
            self.stop()
