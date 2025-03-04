from unittest import TestCase
from src.records.network import Network, DNSRecord
from src.records.record import Record
from src.records.cache import Cache
from src.records.block import TYPE_LOOKUP


class DNSHandlerMock:
    def __init__(self):
        self.protocol = "tcp"


class testNetwork(TestCase):
    def setUp(self):
        Record.initialize()
        Cache.initialize()
        return super().setUp()

    def test_resolve_unkown_domain(self):
        req = DNSRecord.question("no.com", "A")
        reply = req.reply()

        reply = Network.resolve(
            req, reply, "no.com", TYPE_LOOKUP["A"], DNSHandlerMock()
        )
        r = Record.DB
        self.assertEqual(r.get("no.com"), "0")
        self.assertIsNotNone(r.lrange("no.com:1", 0, -1))
