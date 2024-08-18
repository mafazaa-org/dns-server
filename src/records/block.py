from dnslib import RR
from .record import Record
from .answer import Answer


class Block(Record):
    file_name = "blocklist"
    BLOCK_TTL = 4294967295
    answers = [Answer("A", "0.0.0.0", BLOCK_TTL), Answer("AAAA", "::", BLOCK_TTL)]
    regex: str

    def get_answer(self, _type: str) -> RR:
        return super().get_answer(_type, Block.answers)

    @classmethod
    def insert(cls, host: str):
        super().insert(Block(host))

    @classmethod
    def initialize(cls, data: dict):
        cls.regex = data["regex"]
        return super().initialize(data)
