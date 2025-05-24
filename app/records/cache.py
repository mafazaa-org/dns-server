from __future__ import annotations as _annotations

from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from app.constants import LEVEL
from app.db.zones import Zones
from app.db.block import Block
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record_type import RecordType
from re import match
from app.db.group import Group

from ..logger import logger

class Cache(Record):

    regex = "(w{3}\.)?google\..+"
    answers = [
        Answer(1, "216.239.38.120", MAX_TTL), 
        Answer(28,"2001:4860:4802:32::78", MAX_TTL)
        ]
    name = "Cache"
    
    @classmethod
    def initialize(cls):
        # super().initialize()
        
        groups: list[Group] = [Zones(LEVEL), Block(LEVEL)]

        for group in groups:
            logger.d('server',"inserting values for " + group.name)
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
        
    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
        res_data: dict
    ):
        if match(cls.regex, host):
            reply = cls.get_answers(reply, _type, host, cls.answers, handler)
            res_data["google_regex"] = True
            res_data["cache_hit"] = True
            if reply.rr:
                return reply

        
        ## Get cname answer
        cname_key = cls.to_key(host, 5)
        cname_ans = cls.query_db(cname_key)
        cname_ttl = cls.DB.ttl(cname_key)
        cname_answers = map(lambda x: Answer(5, x, cname_ttl), cname_ans)
        
        if len(cname_ans) > 0:
            ttl = cls.DB.ttl(cname_key)
            answers = map(lambda x: Answer(5, x, cname_ttl), cname_ans)
            try:
                reply = cls.get_answers(reply, 5, host, answers, handler)
            except BaseException as e:
                logger.e('error', {
                            "msg": f"error with host {host}",
                            "exception" : e
                        }, handler)
        
        
        ## Ger answer        
        key = cls.to_key(host, _type)
        ans = cls.query_db(key)

        if len(ans) > 0:
            ttl = cls.DB.ttl(key)
            answers = map(lambda x: Answer(_type, x, ttl), ans)
            try:
                reply = cls.get_answers(reply, _type, host, answers, handler)
            except BaseException as e:
                logger.e('error', {
                            "msg": f"error with host {host}",
                            "exception" : e
                        }, handler)
        if reply.rr:
            res_data["cache_hit"] = True
        return reply

        # # no direct zone so look for an SOA record for a higher level zone
        # for record in Record.records:
        #     if record.sub_match(request.q):
        #         reply.add_answer(record.rr)

        # if reply.rr:
        #     print(f"found higher level SOA resource for {request.q.qname}[{type_name}]")
        #     return reply