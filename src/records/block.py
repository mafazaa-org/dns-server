from dnslib import RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from re import match
from sqlite3 import register_adapter, register_converter


class Block(Record):
    table_name = "blocklist"
    answers = [
        Answer("A", "0.0.0.0", MAX_TTL),
        Answer("AAAA", "::", MAX_TTL),
        Answer("NS", "0.0.0.0", MAX_TTL),
        Answer("MX", "0.0.0.0", MAX_TTL),
        Answer("TXT", "None", MAX_TTL),
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
