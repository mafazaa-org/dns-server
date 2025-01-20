from unittest import TestCase, main
from src.records.answer import Answer


class TestAnswer(TestCase):
    def test_init(self):
        a = Answer(5, "www.test.com.", 400)
        self.assertEqual(a._rtype, 5)
        self.assertEqual(a.answer, "www.test.com")
        self.assertEqual(a.ttl, 400)

    def test_validation(self):
        self.assertRaises(ValueError, lambda: Answer(4303, 34, 400))


if __name__ == "__main__":
    main()
