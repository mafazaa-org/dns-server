from dnslib import RR, QTYPE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from re import match
from sqlite3 import register_adapter, register_converter

TYPE_LOOKUP = {
    "A": QTYPE.A,
    "AAAA": QTYPE.AAAA,
    "CAA": QTYPE.CAA,
    "CNAME": QTYPE.CNAME,
    "DNSKEY": QTYPE.DNSKEY,
    "MX": QTYPE.MX,
    "NAPTR": QTYPE.NAPTR,
    "NS": QTYPE.NS,
    "PTR": QTYPE.PTR,
    "RRSIG": QTYPE.RRSIG,
    "SOA": QTYPE.SOA,
    "SRV": QTYPE.SRV,
    "TXT": QTYPE.TXT,
    "SPF": QTYPE.TXT,
}


class Block(Record):
    table_name = "blocklist"
    answers = [
        Answer(TYPE_LOOKUP["A"], "0.0.0.0", MAX_TTL),
        Answer(TYPE_LOOKUP["AAAA"], "::", MAX_TTL),
        Answer(TYPE_LOOKUP["NS"], "0.0.0.0", MAX_TTL),
        Answer(TYPE_LOOKUP["MX"], "0.0.0.0", MAX_TTL),
        Answer(TYPE_LOOKUP["TXT"], "None", MAX_TTL),
    ]
    regex: str

    @classmethod
    def initialize(cls):
        super().initialize()
        register_adapter(bool, int)
        register_converter("BOOLEAN", lambda v: bool(int(v)))
        contains = cls.execute(
            "SELECT * FROM blockregex WHERE is_subdomain == ?",
            (False,),
            callback=lambda x: x.fetchall(),
        )
        subdomains = cls.execute(
            "SELECT * FROM blockregex WHERE is_subdomain == ?",
            (True,),
            callback=lambda x: x.fetchall(),
        )

        cls.regex = cls.create_regex(
            map(lambda x: x[0], contains), map(lambda x: x[0], subdomains)
        )
        cls.run_commiter()

    @classmethod
    def get_answers(
        cls, reply: DNSRecord, _type: str, host: str, handler: DNSHandler
    ) -> RR:
        reply = super().get_answers(
            reply,
            _type,
            host,
            Block.answers,
            handler,
        )
        if not reply.rr:
            reply.add_answer(Answer("CNAME", "block.opendns.com", MAX_TTL).getRR(host))
        return reply

    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        type_name: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        if match(cls.regex, host):
            return cls.get_answers(reply, type_name, host, handler)
        ans = super().query(reply, type_name, host, request, handler)
        if ans:
            return cls.get_answers(reply, type_name, host, handler)
        return reply

    @classmethod
    def create_regex(self, contains: list[str], subdomains: list[str]):
        return f"(.*({'|'.join(contains)}).*)|((.+\.)?({'|'.join(subdomains)})\..+)"
