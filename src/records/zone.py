from dnslib import RR
from .record import Record
from .answer import Answer


class Zone(Record):

    def __init__(self, host, answers: list[Answer]):
        self.answers = answers
        super().__init__(host)

    def get_answer(self, _type: str) -> RR:
        return super().get_answer(_type, self.answers)

    @classmethod
    def insert(cls, host: str, _type: str, _answer: str):
        answer = Answer(_type, _answer)
        super().insert(Zone(host, [answer]))
