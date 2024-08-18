from dnslib import RR
from .record import Record
from .answer import Answer


class Block(Record):
    BLOCK_TTL = 4294967295
    answers = [Answer("A", "0.0.0.0", BLOCK_TTL), Answer("AAAA", "::", BLOCK_TTL)]

    def __init__(self, host):
        super().__init__(host)

    def get_answer(self, _type: str) -> RR:
        return super().get_answer(_type, Block.answers)

    @classmethod
    def insert(cls, host: str):
        super().insert(Block(host))
