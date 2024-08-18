from dnslib.proxy import ProxyResolver as LibProxyResolver
from dnslib import QTYPE
from src.local.record import Record
from src.local.zone import Zone


class ProxyResolver(LibProxyResolver):
    def __init__(self, upstream: str):
        super().__init__(address=upstream, port=53, timeout=5)

    def resolve(self, request, handler):
        answer = _resolve(request)
        if answer:
            return answer

        type_name = QTYPE[request.q.qtype]
        print(f"no local zone found, proxying {request.q.qname}[{type_name}]")
        newZone = super().resolve(request, handler)

        query_type = QTYPE[newZone.q.qtype]
        query_answer = newZone.a.rdata.__str__()

        if query_answer in ["146.112.61.106", "::ffff:9270:3d6a"]:
            host: str = newZone.a.rname.__str__().rstrip(".")
            Record.append(Zone(host=host, type=query_type, answer=query_answer))

        return newZone


def _resolve(request):
    type_name = QTYPE[request.q.qtype]
    reply = request.reply()
    return Record.get_answer(reply, request, type_name)
