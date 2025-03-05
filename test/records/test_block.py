from unittest import TestCase
from app.records.block import Block, TYPE_LOOKUP, MAX_TTL
from app.records.cache import Cache
from app.records.record import Record, DNSRecord


req_types = ["A", "AAAA", "NS", "MX", "TXT"]


class TestBlock(TestCase):

    def setUp(self):
        Block.initialize()
        Record.initialize()
        Cache.initialize()
        return super().setUp()

    def tearDown(self):
        del Block.regex
        return super().tearDown()

    def test_initializing(self):
        self.assertIsNotNone(Block.regex)
        self.assertGreater(len(Block.regex), 10)

    def test_insert_block(self):
        r = Record.DB
        r.delete("surfshark.com")
        self.assertIsNone(r.get("surfshark.com"))

        Block.insert("surfshark.com", "146.112.61.106")
        self.assertEqual(r.get("surfshark.com"), "1")

    def test_insert_allow(self):
        r = Record.DB
        r.delete("surfshark.com")
        self.assertIsNone(r.get("surfshark.com"))

        Block.insert("surfshark.com", "1.1.1.1")
        self.assertEqual(r.get("surfshark.com"), "0")

    def test_get_answers(self):
        for block_domain in [
            "sex",
            "porn",
            "pornhub.com",
            "xvideos.com",
            "tiktok.com",
            "vfdafdatiktokdfaf",
            "4chan.com",
            "motherless.com",
            "surfshark.com",
        ]:
            for req_type_i in range(len(req_types)):
                req = DNSRecord.question(block_domain, req_types[req_type_i])
                reply = req.reply()

                self.assertEqual(
                    Block.get_answers(
                        reply, TYPE_LOOKUP[req_types[req_type_i]], block_domain, {}
                    ).rr[0],
                    Block.answers[req_type_i].getRR(block_domain),
                )

    def test_regex_query(self):

        for block_domain in [
            "sex",
            "porn",
            "pornhub.com",
            "xvideos.com",
            "tiktok.com",
            "vfdafdatiktokdfaf",
        ]:
            for req_type_i in range(len(req_types)):
                req = DNSRecord.question(block_domain, req_types[req_type_i])
                reply = req.reply()

                self.assertEqual(
                    Block.query(
                        reply, TYPE_LOOKUP[req_types[req_type_i]], block_domain, req, {}
                    ).rr[0],
                    Block.answers[req_type_i].getRR(block_domain),
                )

    def test_query_db(self):

        for block_domain in ["4chan.com", "motherless.com", "surfshark.com"]:
            for req_type_i in range(len(req_types)):
                req = DNSRecord.question(block_domain, req_types[req_type_i])
                reply = req.reply()

                self.assertEqual(
                    Block.query(
                        reply, TYPE_LOOKUP[req_types[req_type_i]], block_domain, req, {}
                    ).rr[0],
                    Block.answers[req_type_i].getRR(block_domain),
                )

    def test_query_ttl(self):
        for block_domain in [
            "sex",
            "porn",
            "pornhub.com",
            "xvideos.com",
            "tiktok.com",
            "vfdafdatiktokdfaf",
            "4chan.com",
            "motherless.com",
            "surfshark.com",
        ]:
            for req_type_i in range(len(req_types)):
                req = DNSRecord.question(block_domain, req_types[req_type_i])
                reply = req.reply()

                self.assertEqual(
                    Block.get_answers(reply, req_types[req_type_i], block_domain, {})
                    .rr[0]
                    .ttl,
                    MAX_TTL,
                )
