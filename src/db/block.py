from .group import Group, MAX_TTL


class Block(Group):

    def __init__(self, level):
        self.name = "block"
        super().__init__(level)
        self.list = self.low_raw["list"]
        self.raw = self.low_raw
        self.merge_high()
        self.to_redis = lambda r, value: r.set(value, 1)

    @Group.merge_high_decorator
    def merge_high(self):
        self.list += self.high_raw["list"]
        self.raw = {
            "list": self.low_raw["list"] + self.high_raw["list"],
            "regex": {
                "contains": self.low_raw["regex"]["contains"]
                + self.high_raw["regex"]["contains"],
                "subdomains": self.low_raw["regex"]["subdomains"]
                + self.high_raw["regex"]["subdomains"],
            },
        }

    def get_regex(self):
        return f"(.*({'|'.join(self.raw["regex"]["contains"])}).*)|((.+\.)?({'|'.join(self.raw["regex"]["subdomains"])})\..+)"
