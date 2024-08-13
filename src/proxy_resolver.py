from dnslib.proxy import ProxyResolver as LibProxyResolver
from dnslib import QTYPE
from record import Record
from zone import Zone

class ProxyResolver(LibProxyResolver):
    def __init__(self, records: list[Record], upstream: str, newRecord):
        self.newRecord = newRecord
        self.records = records
        super().__init__(address=upstream, port=53, timeout=5)

    def resolve(self, request, handler):
        answer = _resolve(request, self.records)
        if answer:
            return answer

        type_name = QTYPE[request.q.qtype]
        print(f'no local zone found, proxying {request.q.qname}[{type_name}]')
        newZone =  super().resolve(request, handler)
        
        host : str = newZone.a.rname.__str__().rstrip(".")
        query_type = QTYPE[newZone.q.qtype]
        query_answer = newZone.a.rdata.__str__()
        
        if query_type == 'AAAA' and query_answer ==  '::ffff:9270:3d6a' or query_type == 'A' and query_answer == '146.112.61.106':   
            self.newRecord(host=host, type=query_type, answer=query_answer)
            self.records.append(Record(Zone(host=host,type=query_type, answer=query_answer)))
        
        return newZone
    


def _resolve(request, records : list[Record]):
    type_name = QTYPE[request.q.qtype]
    reply = request.reply()
    for record in records:
        if record.match(request.q):
            reply.add_answer(record.rr)

    if reply.rr:
        print(f'found zone for {request.q.qname}[{type_name}], {len(reply.rr)} replies')
        return reply

    # no direct zone so look for an SOA record for a higher level zone
    for record in records:
        if record.sub_match(request.q):
            reply.add_answer(record.rr)

    if reply.rr:
        print(f'found higher level SOA resource for {request.q.qname}[{type_name}]')
        return reply
