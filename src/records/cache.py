from dnslib import RR, QTYPE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer
from datetime import datetime, timedelta
from threading import Timer


class Cache(Record):
    table_name = "cachelist"
    table2_name = "cache_answers"
    cleaner: Timer

    @classmethod
    def initialize(cls):
        super().initialize()
        # creating
        q = cls.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='zoneslist'",
            callback=lambda x: x.fetchone(),
        )[0].replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        cls.execute(q.replace("zoneslist", cls.table_name))

        q = cls.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='answers'",
            callback=lambda x: x.fetchone(),
        )[0].replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        cls.execute(
            q.replace("answers", cls.table2_name).replace(
                "TEXT NOT NULL",
                "TEXT NOT NULL,\n expire INTEGER NOT NULL",
            )
        )

        cls.execute(f"DELETE FROM {cls.table_name}")
        cls.execute(f"DELETE FROM {cls.table2_name}")
        cls.conn.commit()
        cls.run_cleaner()

    @classmethod
    def run_cleaner(cls):
        cls.cleaner = Timer(60.0, cls.run_cleaner)
        cls.cleaner.start()
        cls.execute(
            f"DELETE FROM {cls.table2_name} WHERE expire <= ?",
            (int(datetime.now().timestamp()),),
        )
        cls.conn.commit()

    @classmethod
    def query(
        cls,
        reply: DNSRecord,
        type_name: RecordType,
        host: str,
        request: DNSRecord,
        handler: DNSHandler,
    ):
        ans = super().query(reply, type_name, host, request, handler)
        if ans:
            return cls.get_answers(reply, type_name, ans, handler)
        return reply

    @classmethod
    def get_answers(
        cls, reply: DNSRecord, _type: str, host: tuple, handler: DNSHandler
    ) -> RR:
        answers = cls.execute(
            f"SELECT type, answer, expire FROM {cls.table2_name} WHERE zone_id = ?",
            (host[0],),
        )
        now = datetime.now().timestamp()
        answers = map(lambda x: Answer(QTYPE[x[0]], x[1], int(x[2] - now)), answers)
        return super().get_answers(reply, _type, host[1], answers, handler)

    @classmethod
    def insert(cls, host, _type: int, answer: str, ttl: int):
        cls.execute(f"INSERT OR IGNORE INTO {cls.table_name}(host) VALUES (?)", (host,))
        id = cls.execute(
            f"SELECT id FROM {cls.table_name} WHERE host=?",
            (host,),
            lambda x: x.fetchone(),
        )[0]

        expire = int((datetime.now() + timedelta(seconds=ttl)).timestamp())

        cls.execute(
            f"INSERT INTO {cls.table2_name}(zone_id, type, answer, expire) VALUES(?, ?, ?, ?)",
            (id, _type, answer, expire),
        )
        cls.conn.commit()
