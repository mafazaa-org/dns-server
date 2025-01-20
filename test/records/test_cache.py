from test.utils.handle_test import handle_test as ht
from dnslib import DNSRecord
from redis import Redis
from src.records.cache import Cache
from src.records.answer import Answer


def __init__():
    Cache.initialize()


def __finish__():
    Cache.r.close()


def wrap_handle_test(func):
    return ht(func, __init__, __finish__)


@wrap_handle_test
def test_insert():
    r: Redis = Cache.r
    rec = DNSRecord.question("www.google.com", "CNAME")
    rec.add_answer(Answer(5, "forcesafesearch.google.com", 300)
                   .getRR("www.google.com"))

    # Ensure any residual data for the test
    if r.exists("www.google.com:5"):
        r.delete("www.google.com:5")

    assert not r.exists("www.google.com")

    Cache.insert("www.google.com", 5, rec.rr)

    assert r.exists("www.google.com:5")
    assert (r.lrange("www.google.com:5", 0, -1)[0]
            == "forcesafesearch.google.com")
    assert r.ttl("www.google.com:5") == 300
