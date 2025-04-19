from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from requests import post
from app.constants import LEVEL, SERVER_HOSTNAME
from app.db.zones import Zones
from app.db.block import Block
from app.db.group import Group


class Cache(Record):

    regex = "(w{3}\.)google\..+"
    answers = [Answer(5, "forcesafesearch.google.com", MAX_TTL)]
    name = "Cache"
    
    @classmethod
    def initialize(cls):
        super().initialize()
        
        groups: list[Group] = [Zones(LEVEL), Block(LEVEL)]

        for group in groups:
            group.insert_values(Record.DB)

        return True

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
            Record.DB.lpush(key, answer)
            Record.DB.expire(key, ans.ttl)

        Record.DB.lpush(main_key, *answers)
        Record.DB.expire(main_key, ttl)