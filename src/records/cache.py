from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer


class Cache(Record):

    @classmethod
    def initialize(cls):
        super().initialize()

    @classmethod
    def insert(cls, host, _type: int, answers: list, ttl: int):

        key = f"{host}:{_type}"
        cls.r.lpush(key, *answers)
        cls.r.expire(key, ttl)
