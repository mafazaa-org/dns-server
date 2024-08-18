from dnslib.proxy import ProxyResolver as LibProxyResolver
from dnslib import QTYPE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from src.records.record import Record
from src.records.zone import Zone
from src.records.block import Block
from src.records.cache import Cache
from src.records.network_cache import NetworkCache


class ProxyResolver(LibProxyResolver):
    def __init__(self, upstream: str):
        super().__init__(address=upstream, port=53, timeout=5)

    def resolve(self, request: DNSRecord, handler: DNSHandler):
        try:
            answer = self._resolve(request)
            if answer:
                return answer
        except:
            ...

        type_name = QTYPE[request.q.qtype]
        print(f"no local zone found, proxying {request.q.qname}[{type_name}]")
        newZone = super().resolve(request, handler)

        host: str = newZone.a.rname.__str__().rstrip(".")
        _type = QTYPE[newZone.q.qtype]
        _answer = newZone.a.rdata.__str__()

        if _answer in ["146.112.61.106", "::ffff:9270:3d6a"]:
            Block.insert(host)
            return newZone

        Cache.insert(host, _type, _answer)
        return newZone

    def _resolve(self, request: DNSRecord):
        type_name = QTYPE[request.q.qtype]
        reply = request.reply()
        for RecordClass in [Cache, NetworkCache, Zone, Block]:
            RecordClass.search(reply, request, type_name)
            if reply.rr:
                return reply
