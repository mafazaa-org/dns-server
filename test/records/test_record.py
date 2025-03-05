from app.records.record import Record
from app.records.answer import Answer
from app.records.cache import Cache
from dnslib import DNSRecord
from unittest import TestCase


class testRecords(TestCase):

    def setUp(self):
        Record.DB.flushall()
        Record.initialize()
        return super().setUp()

    def tearDown(self):
        Record.DB.close()
        return super().tearDown()

    def test_get_answers(self):

        req = DNSRecord.question("www.google.com", "CNAME")
        reply = req.reply()

        google_answers = [Answer(5, "forcesafesearch.google.com", 300)]
        safesearch_answers = [
            Answer(1, "216.1.1.1", 300),
            Answer(28, "ff:ff:ff:ff:", 300),
        ]
        block_answers = [Answer(1, "0.0.0.0", 300), Answer(28, "::", 300)]

        self.assertEqual(
            Record.get_answers(reply, 5, "www.google.com", google_answers, None).rr[0],
            google_answers[0].getRR("www.google.com"),
        )

        self.assertEqual(
            Record.get_answers(reply, 1, "www.google.com", google_answers, None).rr[0],
            google_answers[0].getRR("www.google.com"),
        )

        reply = req.reply()
        self.assertEqual(
            Record.get_answers(
                reply, 1, "forcesafesearch.google.com", safesearch_answers, None
            ).rr[0],
            safesearch_answers[0].getRR("forcesafesearch.google.com"),
        )

        reply = req.reply()
        ans = Record.get_answers(
            reply,
            1,
            "forcesafesearch.google.com",
            [*safesearch_answers, *google_answers],
            None,
        ).rr
        self.assertEqual(
            ans[0], safesearch_answers[0].getRR("forcesafesearch.google.com")
        )
        self.assertEqual(ans[1], google_answers[0].getRR("forcesafesearch.google.com"))

    def test_query(self):

        Record.regex = ""
        Record.answers = []
        Cache.initialize()

        answers = [Answer(5, "restrict.youtube.com", 300)]

        req = DNSRecord.question("youtube.googleapis.com", "CNAME")
        reply = req.reply()

        self.assertEqual(
            Record.query(reply, 5, "youtube.googleapis.com", req, None).rr[0],
            answers[0].getRR("youtube.googleapis.com"),
        )
        del Record.regex
        del Record.answers

    def test_clean_host(self):
        self.assertEqual(Record.clean_host("www.google.com."), "www.google.com")
