from __future__ import annotations as _annotations


from dnslib import QTYPE, RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from redis import Redis
from .record_type import RecordType
from .answer import Answer
from re import match
from os import getenv

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
    def query(
        cls,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        if match(cls.regex, host):
            # print(host, "got matched with regex of ", cls.name)
            reply = cls.get_answers(reply, _type, host, cls.answers, handler)
            if reply.rr:
                return reply

        # print(host, "not matched with regex ", cls.name)
        
        ## Get cname answer
        cname_key = cls.to_key(host, 5)
        cname_ans = cls.query_db(cname_key)
        cname_ttl = cls.DB.ttl(cname_key)
        cname_answers = map(lambda x: Answer(5, x, cname_ttl), cname_ans)
        
        if len(cname_ans) > 0:
            ttl = cls.DB.ttl(cname_key)
            answers = map(lambda x: Answer(5, x, cname_ttl), cname_ans)
            try:
                reply = cls.get_answers(reply, 5, host, answers, handler)
            except BaseException as e:
                print(f"error with host {host}\n{e}")
        
        
        ## Ger answer        
        key = cls.to_key(host, _type)
        ans = cls.query_db(key)

        if len(ans) > 0:
            ttl = cls.DB.ttl(key)
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
    def insert(cls): ...

    @classmethod
    def initialize(cls):
        print("initializing redis cache")
        cls.DB = Redis(REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        cls.DB.flushall()
        print("done initializing redis cache")


    @classmethod
    def clean_host(cls, host: str):
        return host.removesuffix(".")