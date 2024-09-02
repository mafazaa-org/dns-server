from __future__ import annotations as _annotations


from dnslib import QTYPE, RR
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from threading import Lock
from sqlite3 import (
    connect,
    Connection,
    Cursor,
    PARSE_DECLTYPES,
)
from threading import Timer

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


COMMIT_INTERVALS = 10

RecordType = (
    QTYPE.A
    | QTYPE.AAAA
    | QTYPE.CAA
    | QTYPE.CNAME
    | QTYPE.DNSKEY
    | QTYPE.MX
    | QTYPE.NAPTR
    | QTYPE.NS
    | QTYPE.PTR
    | QTYPE.RRSIG
    | QTYPE.SOA
    | QTYPE.SRV
    | QTYPE.TXT
    | QTYPE.SPF
    | QTYPE.HTTPS
)

lock = Lock()


class Record:
    conn: Connection
    crsr: Cursor
    commiter: Timer

    to_string = lambda x: x
    table_name: str

    def sub_match(self, q):
        return self._rtype == QTYPE.SOA and q.qname.matchSuffix(self._rname)

    @classmethod
    def get_answers(
        self,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        answers: list,
        handler: DNSHandler,
    ) -> RR:
        for answer in answers:
            if answer._rtype == _type or answer._rtype == QTYPE.CNAME:
                reply.add_answer(answer.getRR(host))

        return reply

    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        _type: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        return cls.execute(
            f"SELECT * FROM {cls.table_name} WHERE host == '{host}'",
            callback=lambda x: x.fetchone(),
        )

        # # no direct zone so look for an SOA record for a higher level zone
        # for record in Record.records:
        #     if record.sub_match(request.q):
        #         reply.add_answer(record.rr)

        # if reply.rr:
        #     print(f"found higher level SOA resource for {request.q.qname}[{type_name}]")
        #     return reply

    @classmethod
    def execute(cls, sql: str, parameters=(), callback=lambda x: x.fetchall()):
        lock.acquire(True)
        res = callback(cls.crsr.execute(sql, parameters))
        lock.release()
        return res

    @classmethod
    def insert(cls, host):
        cls.execute(f"INSERT INTO {cls.table_name} (host) VALUES (?)", (host,))

    @classmethod
    def initialize(cls, index=True):
        cls.conn = connect(
            "data/data.db", check_same_thread=False, detect_types=PARSE_DECLTYPES
        )
        cls.crsr = cls.conn.cursor()
        if index:
            cls.execute(
                f"CREATE INDEX IF NOT EXISTS hosts_{cls.table_name} ON {cls.table_name} (host);"
            )

    @classmethod
    def run_commiter(cls):
        cls.commiter = Timer(5, cls.run_commiter)
        cls.commiter.start()
        cls.conn.commit()

    @classmethod
    def record_host(cls, request: DNSRecord):
        return cls.clean_host(request.q.qname.__str__())

    @classmethod
    def clean_host(cls, host: str):
        return host.removesuffix(".")
