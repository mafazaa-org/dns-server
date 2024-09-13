from dnslib import RR, QTYPE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from re import match


google_regex = "(w{3}\.)google\..+"
google_answer = Answer(5, "forcesafesearch.google.com", MAX_TTL)


class Zone(Record):
    db_port = 6666

    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        if match(google_regex, host):
            reply.add_answer(google_answer.getRR(host))
            return reply
        ans = super().query(reply, _type, host, request, handler)
        if ans:
            return cls.get_answers(reply, _type, ans, handler)
        return reply
