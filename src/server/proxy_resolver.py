from dnslib.proxy import ProxyResolver as LibProxyResolver
from dnslib import QTYPE, RCODE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from src.utils.constants import DEFAULT_PORT, PROXY_SERVER_TIMEOUT
from src.records.zone import Zone
from src.records.block import Block
from src.records.network import Network
from src.records.record import Record


class ProxyResolver(LibProxyResolver):
    def __init__(self, upstream: str):
        super().__init__(
            address=upstream, port=DEFAULT_PORT, timeout=PROXY_SERVER_TIMEOUT
        )

    def resolve(self, request: DNSRecord, handler: DNSHandler):
        try:
            reply = self._resolve(request, handler)
        except Exception as e:
            print(e)
            reply = request.reply()
            reply.header.rcode = getattr(RCODE, "NXDOMAIN")

        return reply

    def _resolve(self, request: DNSRecord, handler: DNSHandler):
        type_name = QTYPE[request.q.qtype]
        reply = request.reply()
        host = Record.record_host(request)
        for RecordClass in [Zone, Block, Network]:
            if not RecordClass.available:
                print(RecordClass.__name__ + " is not available")
                continue
            reply = (
                RecordClass.search(reply, type_name, host)
                if RecordClass.__name__ != "Network"
                else RecordClass.search(reply, type_name, host, request, handler)
            )
            if reply.rr:
                return reply

        return reply
