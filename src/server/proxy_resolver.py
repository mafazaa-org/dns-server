from dnslib import QTYPE, RCODE, RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from src.utils.constants import DEFAULT_PORT, PROXY_SERVER_TIMEOUT
from .resolve import resolve
from traceback import print_exc


class ProxyResolver:
    def __init__(self, upstream: str):
        self.address = upstream
        self.port = DEFAULT_PORT
        self.timeout = PROXY_SERVER_TIMEOUT

    def resolve(self, request: DNSRecord, handler: DNSHandler):
        reply = request.reply()

        try:
            reply = resolve(request, reply, handler)
        except Exception as e:
            print("exception occured while resolving request")
            print_exc()
            reply.header.rcode = getattr(RCODE, "NXDOMAIN")

        return reply
