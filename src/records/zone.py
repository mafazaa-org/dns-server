from dnslib import RR, QTYPE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from re import match


google_regex = "(w{3}\.)google\..+"
google_answer = Answer("CNAME", "forcesafesearch.google.com", MAX_TTL)


class Zone(Record):
    table_name = "zoneslist"

    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        type_name: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        if match(google_regex, host):
            reply.add_answer(google_answer.getRR(host))
            return reply
        ans = super().query(reply, type_name, host, request, handler)
        if ans:
            return cls.get_answers(reply, type_name, ans, handler)
        return reply

    @classmethod
    def get_answers(
        cls, reply: DNSRecord, _type: str, host: tuple, handler: DNSHandler
    ) -> RR:
        answers = cls.execute(
            "SELECT type, answer FROM answers WHERE zone_id = ?", (host[0],)
        )
        answers = map(lambda x: Answer(QTYPE[x[0]], x[1]), answers)
        return super().get_answers(reply, _type, host[1], answers, handler)
