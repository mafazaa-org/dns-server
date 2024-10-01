from dnslib.dns import DNSRecord, RR
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from re import match


class Cache(Record):

    regex = "(w{3}\.)google\..+"
    answers = [Answer(5, "forcesafesearch.google.com", MAX_TTL)]

    @classmethod
    def insert(cls, host: str, _type: RecordType, rr):
        main_key = cls.to_key(host, _type)
        ttl = rr[0].ttl
        answers = []
        for ans in rr:
            answer = cls.clean_host(ans.rdata.__str__())
            if ans.rtype == _type:
                answers.append(answer)
                ttl = min(ttl, ans.ttl)
                continue

            key = f"{cls.clean_host(ans.rname.__str__())}:{ans.rtype}"
            cls.r.lpush(key, answer)
            cls.r.expire(key, min(cls.r.ttl(key), ans.ttl))

        cls.r.lpush(main_key, *answers)
        cls.r.expire(main_key, ttl)
