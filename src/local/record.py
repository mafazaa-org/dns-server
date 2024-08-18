from __future__ import annotations as _annotations

from datetime import datetime
from textwrap import wrap

from dnslib import QTYPE, RR, DNSLabel, dns
from dnslib.server import DNSServer as LibDNSServer
from json import dump, load

from .zone import Zone

TYPE_LOOKUP = {
    "A": (dns.A, QTYPE.A),
    "AAAA": (dns.AAAA, QTYPE.AAAA),
    "CAA": (dns.CAA, QTYPE.CAA),
    "CNAME": (dns.CNAME, QTYPE.CNAME),
    "DNSKEY": (dns.DNSKEY, QTYPE.DNSKEY),
    "MX": (dns.MX, QTYPE.MX),
    "NAPTR": (dns.NAPTR, QTYPE.NAPTR),
    "NS": (dns.NS, QTYPE.NS),
    "PTR": (dns.PTR, QTYPE.PTR),
    "RRSIG": (dns.RRSIG, QTYPE.RRSIG),
    "SOA": (dns.SOA, QTYPE.SOA),
    "SRV": (dns.SRV, QTYPE.SRV),
    "TXT": (dns.TXT, QTYPE.TXT),
    "SPF": (dns.TXT, QTYPE.TXT),
}

SERIAL_NO = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())


class Record:
    records: list[Record] = []
    zones: list[Zone] = []

    def __init__(self, zone: Zone):
        self._rname = DNSLabel(zone.host)

        rd_cls, self._rtype = TYPE_LOOKUP[zone.type]

        args: list
        if isinstance(zone.answer, str):
            if self._rtype == QTYPE.TXT:
                args = [wrap(zone.answer, 255)]
            else:
                args = [zone.answer]
        else:
            if self._rtype == QTYPE.SOA and len(zone.answer) == 2:
                # add sensible times to SOA
                args = zone.answer + [(SERIAL_NO, 3600, 3600 * 3, 3600 * 24, 3600)]
            else:
                args = zone.answer

        if self._rtype in (QTYPE.NS, QTYPE.SOA):
            ttl = 3600 * 24
        else:
            ttl = 300

        self.rr = RR(
            rname=self._rname,
            rtype=self._rtype,
            rdata=rd_cls(*args),
            ttl=ttl,
        )

    def match(self, q):
        return q.qname == self._rname and (
            q.qtype == QTYPE.ANY or q.qtype == self._rtype
        )

    def sub_match(self, q):
        return self._rtype == QTYPE.SOA and q.qname.matchSuffix(self._rname)

    def __str__(self):
        return str(self.rr)

    @classmethod
    def append(cls, zone: Zone):
        cls.zones.append(zone)
        cls.records.append(Record(zone))

    @classmethod
    def get_answer(cls, reply, request, type_name):
        for record in Record.records:
            if record.match(request.q):
                reply.add_answer(record.rr)

        if reply.rr:
            print(
                f"found zone for {request.q.qname}[{type_name}], {len(reply.rr)} replies"
            )
            return reply

        # no direct zone so look for an SOA record for a higher level zone
        for record in Record.records:
            if record.sub_match(request.q):
                reply.add_answer(record.rr)

        if reply.rr:
            print(f"found higher level SOA resource for {request.q.qname}[{type_name}]")
            return reply

    @classmethod
    def fetch_records(cls):
        return []


def load_records(zones_file: str) -> None:
    with open(zones_file, "r") as rf:
        data = load(rf)

    if not isinstance(data, list):
        raise ValueError(f"Zones must be a list, not {type(data).__name__}")
    Record.zones = [Zone.from_json(i, zone) for i, zone in enumerate(data, start=1)]
    Record.records = [Record(zone) for zone in Record.zones]


def save_records(zones_file: str) -> None:
    with open(zones_file, "w") as wf:
        dump(
            [
                {"host": zone.host, "type": zone.type, "answer": zone.answer}
                for zone in Record.zones
            ],
            wf,
        )
