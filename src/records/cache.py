from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer


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

        if len(ans) > 0:
            ttl = cls.r.ttl(key)
            answers = map(lambda x: Answer(_type, x, ttl), ans)
            try:
                return cls.get_answers(reply, _type, host, answers, handler)
            except BaseException as e:
                print(f"error with host {host}\n{e}")
        return reply

    @classmethod
    def insert(cls, host, _type: int, answers: list, ttl: int):

        key = f"{host}:{_type}"
        cls.r.lpush(key, *answers)
        cls.r.expire(key, ttl)
