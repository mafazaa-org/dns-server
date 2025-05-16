from .group import Group, MAX_TTL
from dnslib import QTYPE
from redis import Redis

TYPE_LOOKUP = {
    "A": QTYPE.A,
    "AAAA": QTYPE.AAAA,
    "CAA": QTYPE.CAA,
    "CNAME": QTYPE.CNAME,
    "DNSKEY": QTYPE.DNSKEY,
    "MX": QTYPE.MX,
    "NAPTR": QTYPE.NAPTR,
    "NS": QTYPE.NS,
    "PTR": QTYPE.PTR,
    "RRSIG": QTYPE.RRSIG,
    "SOA": QTYPE.SOA,
    "SRV": QTYPE.SRV,
    "TXT": QTYPE.TXT,
    "SPF": QTYPE.TXT,
}


class Zones(Group):

    def __init__(self, level):
        self.name = "zones"
        super().__init__(level)
        self.list = self.low_raw
        self.list.append({
		"host": level + ".check.ainaa.mafazaa.com",
		"answers": [{ "type": "CNAME", "answer": "cname.vercel-dns.com" }]
	},)
        self.merge_high()

    @Group.merge_high_decorator
    def merge_high(self):
        self.list += self.high_raw

    def to_redis(self, r: Redis, json: dict):
        done_keys = []
        key = json['host']
        r.set(key, "2")
        for answer in json["answers"]:
            key = json["host"] + ":" + str(TYPE_LOOKUP[answer["type"]])
            if not key in done_keys:
                r.delete(key)
                done_keys.append(key)
            r.lpush(key, answer["answer"])
            r.expire(key, MAX_TTL)
