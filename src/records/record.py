from __future__ import annotations as _annotations


from dnslib import QTYPE, RR
from dnslib.server import DNSServer as LibDNSServer
from dnslib.dns import DNSRecord
from json import dump, load
from re import match

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


RecordType = Literal[
    "A",
    "AAAA",
    "CAA",
    "CNAME",
    "DNSKEY",
    "MX",
    "NAPTR",
    "NS",
    "PTR",
    "RRSIG",
    "SOA",
    "SRV",
    "TXT",
    "SPF",
]


class Record:
    records: list[Record] = []

    available = False
    to_string = lambda x: x

    def __init__(self, host):
        self.host = host

    def match(self, q):
        return match(self.host, q.qname.__str__().rstrip("."))

    def sub_match(self, q):
        return self._rtype == QTYPE.SOA and q.qname.matchSuffix(self._rname)

    def get_answer(self, _type: str, answers: list) -> RR:
        for answer in answers:
            if answer.type == _type:
                return answer.getRR(self.host)

    @classmethod
    def search(cls, reply: DNSRecord, request: DNSRecord, type_name: RecordType):
        for record in cls.records:
            if record.match(request.q):
                rr = record.get_answer(type_name)
                if rr:
                    reply.add_answer(rr)

        # # no direct zone so look for an SOA record for a higher level zone
        # for record in Record.records:
        #     if record.sub_match(request.q):
        #         reply.add_answer(record.rr)

        # if reply.rr:
        #     print(f"found higher level SOA resource for {request.q.qname}[{type_name}]")
        #     return reply

    @classmethod
    def initialize(cls, _hosts: list):
        cls.records: list[Record] = _hosts
        cls.available = True

    @classmethod
    def insert(cls, record: Record):
        cls.records.append(record)

    @classmethod
    def sort(cls):
        cls.available = False
        cls.records.sort(key=cls.to_string)
        cls.available = True
