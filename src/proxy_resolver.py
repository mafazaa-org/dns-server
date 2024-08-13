from dnslib.proxy import ProxyResolver as LibProxyResolver
from records import Records
from dnslib import QTYPE

class ProxyResolver(LibProxyResolver):
    def __init__(self, records: Records, upstream: str):
        self.records = records
        super().__init__(address=upstream, port=53, timeout=5)

    def resolve(self, request, handler):
        answer = resolve(request, handler, self.records)
        if answer:
            return answer

        type_name = QTYPE[request.q.qtype]
        print('no local zone found, proxying %s[%s]', request.q.qname, type_name)
        return super().resolve(request, handler)
    


def resolve(request, handler, records):
    records = [Record(zone) for zone in records.zones]
    type_name = QTYPE[request.q.qtype]
    reply = request.reply()
    for record in records:
        if record.match(request.q):
            reply.add_answer(record.rr)

    if reply.rr:
        print('found zone for %s[%s], %d replies', request.q.qname, type_name, len(reply.rr))
        return reply

    # no direct zone so look for an SOA record for a higher level zone
    for record in records:
        if record.sub_match(request.q):
            reply.add_answer(record.rr)

    if reply.rr:
        print('found higher level SOA resource for %s[%s]', request.q.qname, type_name)
        return reply
