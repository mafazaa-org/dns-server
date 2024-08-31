from dnslib import RR, QTYPE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer
from datetime import datetime, timedelta
from threading import Timer


class Cache(Record):
    table_name = "cachelist"
    cleaner: Timer

    @classmethod
    def initialize(cls):
        super().initialize()
        cls.execute(f"DROP TABLE IF EXISTS {cls.table_name}")

        # creating cachelist table
        q = cls.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='answers'",
            callback=lambda x: x.fetchone(),
        )[0].replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        cls.execute(
            q.replace("answers", cls.table_name).replace(
                "zone_id INTEGER",
                "host TEXT NOT NULL,\n expire INTEGER",
            )
        )
        cls.conn.commit()
        cls.run_cleaner()

    @classmethod
    def run_cleaner(cls):
        cls.cleaner = Timer(60.0, cls.run_cleaner)
        cls.cleaner.start()
        cls.execute(
            f"DELETE FROM {cls.table_name} WHERE expire <= ?",
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

        ans: list[tuple] = cls.execute(
            f"SELECT host, type, answer, expire FROM {cls.table_name} WHERE host=?",
            (host,),
        )
        if len(ans) > 0:
            return cls.get_answers(reply, type_name, ans, handler)
        return reply

    @classmethod
    def get_answers(
        cls,
        reply: DNSRecord,
        _type: str,
        answers_list: list[tuple],
        handler: DNSHandler,
    ) -> RR:
        now = datetime.now().timestamp()
        answers = map(
            lambda x: Answer(QTYPE[x[1]], x[2], int(x[3] - now)), answers_list
        )
        return super().get_answers(reply, _type, answers_list[0][0], answers, handler)

    @classmethod
    def insert(cls, host, _type: int, answer: str, ttl: int):

        expire = int((datetime.now() + timedelta(seconds=ttl)).timestamp())

        cls.execute(
            f"INSERT OR IGNORE INTO {cls.table_name}(host, type, answer, expire) VALUES (?, ?, ?, ?)",
            (host, _type, answer, expire),
        )

        cls.conn.commit()
