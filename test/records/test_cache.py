from dns_server.src.records.cache import Cache
from random import choices
from string import ascii_lowercase
from time import sleep
from datetime import datetime
from random import randint
from ..utils.handle_test import handle_test as ht
from ..utils.get_time import get_time
from dns_server.src.records.record import COMMIT_INTERVALS


def __init__():
    Cache.initialize()


def __finish__():
    Cache.cleaner.cancel()
    Cache.commiter.cancel()
    Cache.conn.close()


handle_test = lambda func: ht(func, __init__, __finish__)


@handle_test
def test_cleaner():
    Cache.insert(
        "should_expire_now.com",
        5,
        "www.should_expire_now.com",
        int(datetime.now().timestamp()),
    )

    Cache.insert(
        "should_expire_after_fifteen_seconds.com",
        5,
        "www.should_expire_after_fifteen_seconds.com",
        int(datetime.now().timestamp()),
    )
    sleep(0.1)
    Cache.run_cleaner()
    assert (
        len(
            Cache.execute(
                "SELECT * FROM cachelist WHERE host=?", ("should_expire_now.com",)
            )
        )
        == 0
    )
    sleep(16)
    assert len(Cache.execute("SELECT * FROM cachelist")) == 0


@handle_test
def test_heavy():

    amounts = [50, 400, 800]
    amount_records = [x**3 for x in amounts]

    gen_random = lambda x: [
        ["".join(choices(ascii_lowercase, k=5)) for _ in range(x)] for _ in range(3)
    ]

    for i in range(len(amounts)):
        amount = amounts[i]
        records = "{:,}".format(amount_records[i])
        random_domains = gen_random(amount)
        __init__()

        get_time(
            lambda: insert_random(random_domains),
            f"{records} records test_cache/test_heavy/insertions",
        )()
        sleep(COMMIT_INTERVALS)

        get_time(
            lambda: Cache.execute(
                "SELECT * FROM cachelist WHERE host=?",
                (
                    f"{random_domains[0][randint(0, amount - 1)]}.{random_domains[1][randint(0, amount - 1)]}.{random_domains[2][randint(0, amount - 1)]}",
                ),
            ),
            f"{records} records test_cache/test_heavy/single_query",
        )()

        Cache.conn.commit()
        get_time(
            insert,
            f"{records} records test_cache/test_heavy/single_insert",
        )()

        __finish__()


def insert():
    Cache.insert(f"test.com", 5, "www.test.com", int(datetime.now().timestamp() + 300))
    Cache.conn.commit()


def insert_random(random_domains):
    expire = int(datetime.now().timestamp() + 6000)
    for subdomain in random_domains[0]:
        for domain in random_domains[1]:
            for tld in random_domains[2]:
                Cache.insert(f"{subdomain}.{domain}.{tld}", 5, "www.test.com", expire)

    assert Cache.execute(
        "SELECT COUNT(host) FROM cachelist", callback=lambda x: x.fetchone()
    )[0] == (len(random_domains[0]) ** 3)
