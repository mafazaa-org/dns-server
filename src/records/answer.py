from __future__ import annotations as _annotations

from re import sub
from datetime import datetime
from textwrap import wrap

from dnslib import QTYPE, RR, dns
from .record import RecordType

RECORD_TYPES = RecordType.__args__

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

MAX_TTL = 4294967295


class Answer:
    def __init__(self, _type: RecordType, _answer, ttl=None) -> None:
        self.type = _type
        self.answer = _answer

        self.rd_cls, self._rtype = TYPE_LOOKUP[_type]

        self.args: list
        if isinstance(_answer, str):
            if self._rtype == QTYPE.TXT:
                self.args = [wrap(_answer, 255)]
            else:
                self.args = [_answer]
        else:
            if self._rtype == QTYPE.SOA and len(_answer) == 2:
                # add sensible times to SOA
                self.args = _answer + [(SERIAL_NO, 3600, 3600 * 3, 3600 * 24, 3600)]
            else:
                self.args = _answer

        self.ttl = (
            ttl if ttl else 3600 * 24 if self._rtype in (QTYPE.NS, QTYPE.SOA) else 300
        )

    def getRR(self, _rname):
        return RR(
            rname=_rname, rtype=self._rtype, rdata=self.rd_cls(*self.args), ttl=self.ttl
        )

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type: str):
        if _type not in RECORD_TYPES:
            raise ValueError(
                f'Zone {self.host} is invalid, "type" must be one of {", ".join(RECORD_TYPES)}, got {type!r}'
            )
        self._type = _type

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, _answer: str | list):
        if isinstance(_answer, str):
            _answer = sub(r"\s*\r?\n", "", _answer)
        elif not isinstance(_answer, list) or not all(
            isinstance(x, (str, int)) for x in _answer
        ):
            raise ValueError(
                f'Zone {self.host} is invalid, "answer" must be a string or list of strings and ints, got {_answer!r}'
            )
        self._answer = _answer
