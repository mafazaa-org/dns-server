from dnslib import RR, QTYPE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from re import match
from requests import get
from app.constants import LEVEL
from app.db.block import Block as Block_db

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
    "HTTPS": QTYPE.HTTPS,
}


class Block(Record):
    global DB
    
    name = "Block"
    answers = [
        Answer(TYPE_LOOKUP["A"], "0.0.0.0", MAX_TTL),
        Answer(TYPE_LOOKUP["AAAA"], "::", MAX_TTL),
        Answer(TYPE_LOOKUP["NS"], "0.0.0.0", MAX_TTL),
        Answer(TYPE_LOOKUP["MX"], "0.0.0.0", MAX_TTL),
        Answer(TYPE_LOOKUP["TXT"], "None", MAX_TTL),
    ]
    regex: str

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
            reply.add_answer(
                Answer(TYPE_LOOKUP["CNAME"], "block.ainaa.mafazaa.com", MAX_TTL).getRR(
                    host
                )
            )
        return reply

    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        #TODO fix this to clean host
        if match(cls.regex, host) or Record.DB.get(host) == "1":
            return cls.get_answers(reply, _type, host, handler)
        return reply

    @classmethod
    def insert(cls, host, answer):

        disable = answer in [
            "146.112.61.106",
            "::ffff:9270:3d6a",
            "::ffff:146.112.61.104",
            "146.112.61.104",
        ]

        Record.DB.set(
            host,
            (1 if disable else 0),
        )
        return disable

    @classmethod
    def initialize(cls):
        # super().initialize()
        cls.regex = Block_db(LEVEL).get_regex()
        return True
