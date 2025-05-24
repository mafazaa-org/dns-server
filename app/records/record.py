from __future__ import annotations as _annotations


from dnslib import QTYPE, RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from redis import Redis
from .record_type import RecordType
from .answer import Answer
from re import match
from os import getenv
from ..logger import logger

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')

# REDIS_HOST, REDIS_PORT


class Record:

    to_string = lambda x: x
    to_key = lambda host, _type: f"{host}:{_type}"
    DB: Redis
    query_db = lambda key: Record.DB.lrange(key, 0, -1)
    name : str

    regex: str
    answers: list[Answer]

    def sub_match(self, q):
        return self._rtype == QTYPE.SOA and q.qname.matchSuffix(self._rname)

    @classmethod
    def get_answers(
        self,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        answers: list[Answer],
        handler: DNSHandler,
    ) -> RR:
        for answer in answers:
            if answer._rtype == _type or answer._rtype == QTYPE.CNAME:
                reply.add_answer(answer.getRR(host))

        return reply


    @classmethod
    def insert(cls): ...

    @classmethod
    def initialize(cls):
        logger.d('server',"initializing redis cache")
        cls.DB = Redis(REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        cls.DB.flushall()
        logger.d('server', "done initializing redis cache")


    @classmethod
    def clean_host(cls, host: str):
        return host.removesuffix(".")