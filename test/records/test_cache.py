from app.records.cache import Cache
from app.records.answer import Answer
from app.records.record import Record
from dnslib import DNSRecord
from redis import Redis
from unittest import TestCase


class testCache(TestCase):

    def setUp(self):
        Record.initialize()
        Record.DB.flushall()
        return super().setUp()

    def tearDown(self):
        Record.DB.close()
        return super().tearDown()

    def test_initializing(self):
        Record.DB.flushall()
        self.assertTrue(Cache.initialize())

        r: Redis = Record.DB
        self.assertGreater(len(r.keys("*")), 0)

    def test_insert(self):

        Cache.initialize()

        r: Redis = Record.DB
        rec = DNSRecord.question("www.google.com", "CNAME")
        rec.add_answer(
            Answer(5, "forcesafesearch.google.com", 300).getRR("www.google.com")
        )

        if r.exists("www.google.com:5"):
            r.delete("www.google.com:5")

        self.assertFalse(r.exists("www.google.com"))
        Cache.insert("www.google.com", 5, rec.rr)
        self.assertTrue(r.exists("www.google.com:5"))
        self.assertEqual(
            r.lrange("www.google.com:5", 0, -1)[0], "forcesafesearch.google.com"
        )
        self.assertEqual(r.ttl("www.google.com:5"), 300)

    def test_multiple_inserts(self): ...
