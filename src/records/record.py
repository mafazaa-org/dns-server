from __future__ import annotations as _annotations


from dnslib import QTYPE, RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from redis import Redis
from .record_type import RecordType
from .answer import Answer

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


COMMIT_INTERVALS = 1


class Record:

    to_string = lambda x: x
    db_port = 6379
    db_host = "localhost"

    def sub_match(self, q):
        return self._rtype == QTYPE.SOA and q.qname.matchSuffix(self._rname)

    @classmethod
    def get_answers(
        self,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        answers: list,
        handler: DNSHandler,
    ) -> RR:
        for answer in answers:
            if answer._rtype == _type or answer._rtype == QTYPE.CNAME:
                reply.add_answer(answer.getRR(host))

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
        key = f"{host}:{_type}"
        ans = cls.r.lrange(key, 0, -1)

        if len(ans) > 0:
            ttl = cls.r.ttl(key)
            answers = map(lambda x: Answer(_type, x, ttl), ans)
            try:
                return cls.get_answers(reply, _type, host, answers, handler)
            except BaseException as e:
                print(f"error with host {host}\n{e}")
        return reply

        # # no direct zone so look for an SOA record for a higher level zone
        # for record in Record.records:
        #     if record.sub_match(request.q):
        #         reply.add_answer(record.rr)

        # if reply.rr:
        #     print(f"found higher level SOA resource for {request.q.qname}[{type_name}]")
        #     return reply

    @classmethod
    def insert(cls, host): ...

    @classmethod
    def initialize(cls):
        cls.r = Redis(cls.db_host, port=cls.db_port, decode_responses=True)

    @classmethod
    def record_host(cls, request: DNSRecord):
        return cls.clean_host(request.q.qname.__str__())

    @classmethod
    def clean_host(cls, host: str):
        return host.removesuffix(".")
