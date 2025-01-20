from traceback import print_exc
from dnslib import RCODE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from src.constants import DEFAULT_PORT
from src.server.resolve import resolve


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
