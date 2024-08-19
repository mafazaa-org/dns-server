from dnslib import RR
from .record import Record, RecordType
from .block import Block
from .zone import Zone
from .answer import Answer
from dnslib import DNSRecord, QTYPE, RCODE
from dnslib.server import DNSHandler
from socket import timeout
from ..utils.constants import DEFAULT_PORT, server, PROXY_SERVER_TIMEOUT


class Network(Record):
    file_name = "network"
    available = True

    def __init__(self, host, answers: list[Answer]):
        self.answers = answers
        super().__init__(host)

    def get_answer(self, _type: str) -> RR:
        return super().get_answer(_type, self.answers)

    @classmethod
    def insert(cls, host: str, _type: str, _answer: str):
        answer = Answer(_type, _answer)
        super().insert(Network(host, [answer]))

    @classmethod
    def from_json(cls, json: dict):

        return cls(json["host"], [Answer.from_json(x) for x in json["answers"]])

    @classmethod
    def search(
        cls,
        reply: DNSRecord,
        type_name: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        return cls.resolve(request, handler)

    @classmethod
    def resolve(cls, request: DNSRecord, handler: DNSHandler):
        if handler.protocol == "udp":
            proxy_r = request.send(server, DEFAULT_PORT, timeout=PROXY_SERVER_TIMEOUT)
        else:
            proxy_r = request.send(
                server, DEFAULT_PORT, tcp=True, timeout=PROXY_SERVER_TIMEOUT
            )
        reply = DNSRecord.parse(proxy_r)

        cls.insert(reply)

        return reply

    @classmethod
    def insert(cls, reply: DNSRecord):
        host: str = reply.a.rname.__str__().rstrip(".")
        _type = QTYPE[reply.q.qtype]
        _answer = reply.a.rdata.__str__()

        if _answer in ["146.112.61.106", "::ffff:9270:3d6a"]:
            Block.insert(host)
            return reply

        Zone.insert(host, _type, _answer)
