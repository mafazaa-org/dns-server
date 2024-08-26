from dnslib import DNSRecord, QTYPE, RR, DNSQuestion
from dnslib.server import DNSHandler
from src.records.record import Record
from src.records.zone import Zone
from src.records.block import Block
from src.records.network import Network


def resolve(request: DNSRecord, reply: DNSRecord, handler: DNSHandler):
    # get type name, reply and clean host
    type_name = QTYPE[request.q.qtype]
    host = Record.record_host(request)

    # for recordclass in recordclasses
    for RecordClass in [Zone, Block, Network]:

        # query
        reply: DNSRecord = RecordClass.query(reply, type_name, host, request, handler)
        if not reply.rr:
            continue

        for rr in reply.rr:
            if rr.rtype != 5 and type_name in ["A", "AAAA"]:
                continue
            try:
                q = DNSRecord(
                    q=DNSQuestion(qname=rr.rdata.__str__(), qtype=request.q.qtype)
                )
            except UnicodeError:
                print("\n\n\nthere was an error while encoding\n\n\n")
                return reply
            cname_reply = q.reply()
            cname_reply = resolve(
                q,
                cname_reply,
                handler,
            )
            reply.rr.extend(cname_reply.rr)

        return reply

    return reply
