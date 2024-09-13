from dnslib import RR
from .record import Record, RecordType
from .block import Block
from .cache import Cache
from dnslib import DNSRecord, DNSError
from dnslib.server import DNSHandler
from socket import timeout
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
        type_name: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        return cls.resolve(request, reply, handler)

    @classmethod
    def resolve(cls, request: DNSRecord, reply: DNSRecord, handler: DNSHandler):
        try:
            if handler.protocol == "udp":
                proxy_r = request.send(
                    server, DEFAULT_PORT, timeout=PROXY_SERVER_TIMEOUT
                )
            else:
                proxy_r = request.send(
                    server, DEFAULT_PORT, tcp=True, timeout=PROXY_SERVER_TIMEOUT
                )

            res = DNSRecord.parse(proxy_r)
            cls.insert(res)
            return res
        except:
            ...

    @classmethod
    def insert(cls, reply: DNSRecord):
        try:
            host: str = cls.clean_host(reply.a.rname.__str__())
        except DNSError:
            return
        answer = reply.a.rdata.__str__()

        if answer in ["146.112.61.106", "::ffff:9270:3d6a"]:
            Block.insert(host)
            return

        for ans in reply.rr:
            Cache.insert(
                cls.clean_host(ans.rname.__str__()),
                ans.rtype,
                ans.rdata.__str__(),
                ans.ttl,
            )
