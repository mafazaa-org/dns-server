from dnslib import RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer
from datetime import datetime


class Cache(Record):

    @classmethod
    def initialize(cls):
        super().initialize(False)

    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        type_name: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):

        ans: list[tuple] = cls.execute(
            f"SELECT host, type, answer, expire FROM {cls.table_name} WHERE host=?",
            (host,),
        )
        if len(ans) > 0:
            try:
                return cls.get_answers(reply, type_name, ans, handler)
            except BaseException as e:
                print(f"error with host {host}\n{e}")
        return reply

    @classmethod
    def get_answers(
        cls,
        reply: DNSRecord,
        _type: str,
        answers_list: list[tuple],
        handler: DNSHandler,
    ) -> RR:
        now = datetime.now().timestamp()
        answers = map(lambda x: Answer(x[1], x[2], int(x[3] - now)), answers_list)
        return super().get_answers(reply, _type, answers_list[0][0], answers, handler)

    @classmethod
    def insert(cls, host, _type: int, answer: str, ttl: int):

        ...
