from redis import Redis
from os.path import join
from json import load, dump

MAX_TTL = 4294967295


class Group:

    def __init__(self, level) -> None:
        self.list: list
        self.low_raw: dict
        self.high_raw: dict
        self.raw: dict
        self.name: str
        self.level = level
        self.to_redis: function
        self.get_raw()

    def insert_values(self, r: Redis):
        for value in self.list:
            self.to_redis(r, value)

    def get_raw(self):
        self.low_raw = load(
            open(join("source_data", "low", f"{self.name}.json"), encoding="utf-8")
        )
        if self.level != "high":
            return
        self.high_raw = load(
            open(join("source_data", "high", f"{self.name}.json"), encoding="utf-8")
        )

    def update_file(self):
        dump(
            self.raw,
            open(
                join("updated_data", self.level, f"{self.name}.json"),
                encoding="utf-8",
                mode="w",
            ),
        )

    @classmethod
    def merge_high_decorator(cls, func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                ...

        return wrapper
