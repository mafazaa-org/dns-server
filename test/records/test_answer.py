from app.records.answer import Answer, RR, TYPE_LOOKUP, DEFAULT_TTL
from unittest import TestCase, main


class TestAnswer(TestCase):
    def test_init(self):
        a = Answer(5, "www.test.com.", 400)
        self.assertEqual(a._rtype, 5)
        self.assertEqual(a.answer, "www.test.com")
        self.assertEqual(a.ttl, 400)

    def test_validation(self):
        self.assertRaises(ValueError, lambda: Answer(4303, 34, 400))

    def test_default_ttl(self):
        a = Answer(5, "www.test.com")
        self.assertEqual(a.ttl, DEFAULT_TTL)
        self.assertEqual(
            a.getRR("www.google.com"),
            RR(
                "www.google.com",
                rtype=5,
                rdata=TYPE_LOOKUP[5](("www.test.com")),
                ttl=DEFAULT_TTL,
            ),
        )

    def test_getRR(self):
        a = Answer(5, "forcesafesearch.google.com", 4000)
        self.assertEqual(
            a.getRR("www.google.com"),
            RR(
                "www.google.com",
                rtype=5,
                rdata=TYPE_LOOKUP[5](("forcesafesearch.google.com")),
                ttl=4000,
            ),
        )


if __name__ == "__main__":
    main()
