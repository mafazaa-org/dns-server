from dnslib import RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer
from datetime import datetime


class Cache(Record):

    @classmethod
    def initialize(cls):
        super().initialize()

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
        
        print(ans)

        if len(ans) > 0:
            ttl = cls.r.ttl(key)
            answers = map( lambda x: Answer(_type, x, ttl) ,ans)
            try:
                return cls.get_answers(reply, _type, host, answers, handler)
            except BaseException as e:
                print(f"error with host {host}\n{e}")
        return reply

    @classmethod
    def insert(cls, host, _type: int, answer: str, ttl: int):

        ...
