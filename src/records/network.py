from dnslib import RR
from .record import Record, RecordType
from .block import Block
from .cache import Cache
from dnslib import DNSRecord, DNSError
from dnslib.server import DNSHandler
from ..utils.constants import DEFAULT_PORT, PROXY_SERVER_TIMEOUT, server


class Network(Record):
    table_name = None

    @classmethod
    def get_answers(
        cls, reply: DNSRecord, _type: str, host: str, handler: DNSHandler
    ) -> RR:
        return super().get_answers(
            reply,
            _type,
            host,
            cls.answers,
            handler,
        )

    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        return cls.resolve(request, reply, host, _type, handler)

    @classmethod
    def resolve(
        cls,
        request: DNSRecord,
        reply: DNSRecord,
        host: str,
        _type: RecordType,
        handler: DNSHandler,
    ):
        try:
            if handler.protocol == "udp":
                proxy_r = request.send(
                    server, DEFAULT_PORT, timeout=PROXY_SERVER_TIMEOUT
                )
            else:
                proxy_r = request.send(
                    server, DEFAULT_PORT, tcp=True, timeout=PROXY_SERVER_TIMEOUT
                )

            reply = DNSRecord.parse(proxy_r)
            cls.insert(reply, host, _type)
        except BaseException as e:
            raise e
        finally:
            return reply

    @classmethod
    def insert(cls, reply: DNSRecord, host: str, _type: RecordType):
        answer = reply.a.rdata.__str__()

        if answer in ["146.112.61.106", "::ffff:9270:3d6a"]:
            Block.insert(host)
            return

        Cache.insert(host, _type, reply.rr)
