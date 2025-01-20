from __future__ import annotations as _annotations
from re import match
import os
from dnslib import QTYPE, RR
from dnslib.dns import DNSRecord
from redis import Redis
from dotenv import load_dotenv
from src.records.record_type import RecordType
from src.records.answer import Answer

load_dotenv()


class Record:

    to_string = lambda x: x  # noqa: E731
    to_key = lambda host, _type: f"{host}:{_type}"  # noqa: E731
    DB: Redis
    query_db = lambda key: Record.DB.lrange(key, 0, -1)  # noqa: E731

    # Make regex a string with a default fallback
    regex: str = os.getenv('REGEX') or ""
    answers: list[Answer] = [Answer(5, "forcesafesearch.google.com", 300)]

    def __init__(self):
        self._rtype = None  # Initialize rtype
        self._rname = None  # Initialize rname

    def sub_match(self, q) -> bool:
        return self._rtype == QTYPE.SOA and q.qname.matchSuffix(self._rname)

    @classmethod
    def get_answers(
        cls,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        answers: list[Answer]
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
        host: str
    ) -> DNSRecord:
        if match(cls.regex, host):
            reply = cls.get_answers(reply, _type, host, cls.answers)
            if reply.rr:
                return reply

        key = cls.to_key(host, _type)
        ans = cls.query_db(key)

        if ans:  # Check if ans is non-empty
            ttl = cls.DB.ttl(key)
            answers = list(map(lambda x: Answer(_type, x, ttl), ans))
            # Convert map to list
            try:
                return cls.get_answers(reply, _type, host, answers)
            except Exception as e:  # Catch only general exceptions
                print(f"error with host {host}\n{e}")
        return reply

    @classmethod
    def initialize(cls):
        cls.DB = Redis(os.getenv('REDIS_HOST'),
                       port=int(os.getenv('REDIS_PORT')),
                       decode_responses=True)

    @classmethod
    def clean_host(cls, host: str) -> str:
        return host.removesuffix(".")
