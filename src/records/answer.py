from __future__ import annotations as _annotations

from re import sub
from datetime import datetime
from textwrap import wrap

from dnslib import QTYPE, RR, dns
from .record import RecordType

TYPE_LOOKUP = {
    QTYPE.A: dns.A,
    QTYPE.AAAA: dns.AAAA,
    QTYPE.CAA: dns.CAA,
    QTYPE.CNAME: dns.CNAME,
    QTYPE.DNSKEY: dns.DNSKEY,
    QTYPE.MX: dns.MX,
    QTYPE.NAPTR: dns.NAPTR,
    QTYPE.NS: dns.NS,
    QTYPE.PTR: dns.PTR,
    QTYPE.RRSIG: dns.RRSIG,
    QTYPE.SOA: dns.SOA,
    QTYPE.SRV: dns.SRV,
    QTYPE.TXT: dns.TXT,
    QTYPE.HTTPS: dns.HTTPS,
}

SERIAL_NO = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())

MAX_TTL = 4294967295

DEFAULT_TTL = 60 * 1


class Answer:
    def __init__(self, _type: RecordType, _answer, ttl=None) -> None:
        self.answer = _answer
        self._rtype = _type

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
            ttl
            if ttl and ttl > 0
            else 3600 * 24 if self._rtype in (QTYPE.NS, QTYPE.SOA) else DEFAULT_TTL
        )

    def getRR(self, _rname):
        return RR(
            rname=_rname,
            rtype=self._rtype,
            rdata=TYPE_LOOKUP[self._rtype](*self.args),
            ttl=self.ttl,
        )

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
