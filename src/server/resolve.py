from dnslib import DNSRecord, QTYPE, RR, DNSQuestion
from dnslib.server import DNSHandler
from src.records.record import Record
from src.records.zone import Zone
from src.records.block import Block
from src.records.cache import Cache
from src.records.network import Network

RecordClasses: list[Record] = [Cache, Zone, Block, Network]


def resolve(request: DNSRecord, reply: DNSRecord, handler: DNSHandler, first_time=True):
    # get type name, reply and clean host
    _type = request.q.qtype
    host = Record.record_host(request)

    # for recordclass in recordclasses
    for RecordClass in RecordClasses:
        # query
        reply: DNSRecord = RecordClass.query(reply, _type, host, request, handler)
        if not reply.rr:
            continue

        if not first_time or request.q.qtype == QTYPE.CNAME:
            return reply

        for rr in reply.rr:
            if rr.rtype != 5 and _type in [QTYPE.A, QTYPE.AAAA]:
                continue
            try:
                q = DNSRecord(
                    q=DNSQuestion(qname=rr.rdata.__str__(), qtype=request.q.qtype)
                )
            except UnicodeError:
                print("\n\n\nthere was an error while encoding\n\n\n")
                return reply
            cname_reply = q.reply()
            cname_reply = resolve(q, cname_reply, handler, first_time=False)
            reply.rr.extend(cname_reply.rr)

        return reply

    return reply
