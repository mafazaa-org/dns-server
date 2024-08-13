from __future__ import annotations as _annotations

from dnslib.server import DNSServer as LibDNSServer
from records import load_records
from proxy_resolver import ProxyResolver
from zone import Zone
from typing import List

DEFAULT_PORT = 53
class DnsServer():
    def __init__(self, upstream : str) -> None:
        self.upstream = upstream
        self.udp_server : LibDNSServer | None = None
        self.tcp_server : LibDNSServer | None = None
        self.records = load_records("src/zones.toml")
        

    def start(self):
        print('starting DNS server on port %d, upstream DNS server "%s"', DEFAULT_PORT, self.upstream)
        resolver = ProxyResolver(self.records, self.upstream)
        
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
        return (self.udp_server and self.udp_server.isAlive()) or (self.tcp_server and self.tcp_server.isAlive())

    def add_record(self, zone: Zone):
        self.records.zones.append(zone)

    def set_records(self, zones: List[Zone]):
        self.records.zones = zones
        