
from dnslib import DNSRecord, QTYPE, DNSQuestion, RR
from dnslib.server import DNSHandler
from app.records.record import Record
from app.records.block import Block
from app.records.cache import Cache
from app.records.network import Network

RecordClasses: list[Record] = [Cache, Block, Network]


def resolve(request: DNSRecord, reply: DNSRecord, handler: DNSHandler, host: str, _type: int, res_data: dict, first_time=True):
    # get type name, reply and clean host
    # for recordclass in recordclasses
    for RecordClass in RecordClasses:
        # query
        reply: DNSRecord = RecordClass.query(reply, _type, host, request, handler, res_data)
        if not reply.rr:
            continue

        if not first_time or request.q.qtype == QTYPE.CNAME:
            return reply

        copied_rr = [x for x in reply.rr]
        for rr in copied_rr:
            if rr.rtype != 5 and _type in [QTYPE.A, QTYPE.AAAA]:
                continue
            try:
                q = DNSRecord(
                    q=DNSQuestion(qname=rr.rdata.__str__(), qtype=request.q.qtype)
                )
            except UnicodeError:
                return reply
            cname_reply = q.reply()
            cname_reply = resolve(q, cname_reply, handler,rr.rdata.__str__(), _type, res_data, False)
            reply.rr.extend(cname_reply.rr)
            
        return reply

    return reply
