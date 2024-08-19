from dnslib import RR
from dnslib.dns import DNSRecord
from .record import Record, RecordType
from .answer import Answer
from re import match


class Block(Record):
    file_name = "blocklist"
    BLOCK_TTL = 4294967295
    answers = [Answer("A", "0.0.0.0", BLOCK_TTL), Answer("AAAA", "::", BLOCK_TTL)]

    def get_answer(self, _type: str, host: str) -> RR:
        return super().get_answer(_type, host, Block.answers)

    @classmethod
    def search(cls, reply: DNSRecord, type_name: RecordType, host: str):
        if cls.regex.match(host):
            reply.add_answer(cls.regex.get_answer(type_name, host))
            return reply
        return super().search(reply, type_name, host)

    @classmethod
    def insert(cls, host: str):
        super().insert(Block(host))

    @classmethod
    def initialize(cls, data: dict):
        cls.regex: Block = cls(data["regex"])
        return super().initialize(data)

    @classmethod
    def from_json(cls, json: dict):
        return cls(json)
