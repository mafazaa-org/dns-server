import os
from requests import post
from dotenv import load_dotenv
from src.records.record import Record
from src.records.answer import Answer, MAX_TTL

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
DB_ADDR = os.getenv('DB_ADDR')
LEVEL = os.getenv('LEVEL')
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME')


class Cache(Record):
    regex = r"(www\.)?google\..+"
    answers = [Answer(5, "forcesafesearch.google.com", MAX_TTL)]

    @classmethod
    def initialize(cls):
        """Initialize the cache by fetching data from the database."""
        super().initialize()
        res = post(
            f"{DB_ADDR}/update/redis?level={LEVEL}&server={SERVER_HOSTNAME}",
            timeout=5  # Added timeout to prevent hanging
        ).json()

        if res["status"] != "success":
            raise Exception("Couldn't fetch data from db")

        print("Fetched data successfully")

    @classmethod
    def insert(cls, host: str, rr):
        """Insert records into Cache."""
        _type = rr[0].rtype  # Assuming all records in rr are of the same type
        main_key = cls.to_key(host, _type)
        ttl = rr[0].ttl
        answers = []

        for ans in rr:
            answer = cls.clean_host(str(ans.rdata))
            if ans.rtype == _type:
                answers.append(answer)
                ttl = min(ttl, ans.ttl)
            else:
                key = f"{cls.clean_host(str(ans.rname))}:{ans.rtype}"
                Record.DB.lpush(key, answer)
                Record.DB.expire(key, min(Record.DB.ttl(key), ans.ttl))

        Record.DB.lpush(main_key, *answers)
        Record.DB.expire(main_key, ttl)  # Use the calculated ttl
