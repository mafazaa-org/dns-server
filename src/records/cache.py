from .record import Record, RecordType
from .answer import Answer, MAX_TTL
from requests import post
from src.env import DB_ADDR, LEVEL, SERVER_HOSTNAME


class Cache(Record):

    regex = "(w{3}\.)google\..+"
    answers = [Answer(5, "forcesafesearch.google.com", MAX_TTL)]

    @classmethod
    def initialize(cls):
        super().initialize()
        res = post(
            f"{DB_ADDR}/update/redis?level={LEVEL}&server={SERVER_HOSTNAME}"
        ).json()
        if res["status"] != "success":
            raise Exception("Couldn't fetch data from db")

        print("Fetched data successfully")

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
            Record.DB.expire(key, min(Record.DB.ttl(key), ans.ttl))

        Record.DB.lpush(main_key, *answers)
        Record.DB.expire(main_key, ttl)
