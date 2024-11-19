from dnslib import QTYPE, RCODE, RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from src.env import DEFAULT_PORT
from .resolve import resolve
from traceback import print_exc


class ProxyResolver:
    def __init__(self):
        self.port = DEFAULT_PORT

    def resolve(self, request: DNSRecord, handler: DNSHandler):
        reply = request.reply()

        try:
            reply = resolve(request, reply, handler)
        except Exception:
            print("\n\nexception occured while resolving request\n\n")
            print_exc()
            print("\n\nend of exception\n\n")
            reply.header.rcode = getattr(RCODE, "NXDOMAIN")

        return reply
