from test.utils.handle_test import handle_test as ht
from dnslib import DNSRecord
from src.records.record import Record
from src.records.answer import Answer


def __init__():
    Record.initialize()


def __finish__():
    Record.r.close()


def handle_test(x):
    return ht(x, __init__, __finish__)


@handle_test
def test_get_answers():

    req = DNSRecord.question("www.google.com", "CNAME")
    reply = req.reply()

    google_answers = [Answer(5, "forcesafesearch.google.com", 300)]
    safesearch_answers = [Answer(1, "216.1.1.1", 300),
                          Answer(28, "ff:ff:ff:ff:", 300)]

    assert Record.get_answers(reply, 5,
                              "www.google.com",
                              google_answers, None).rr[
        0
    ] == google_answers[0].getRR("www.google.com")

    assert Record.get_answers(reply, 1,
                              "www.google.com",
                              google_answers, None).rr[
        0
    ] == google_answers[0].getRR("www.google.com")

    reply = req.reply()
    assert Record.get_answers(
        reply, 1, "forcesafesearch.google.com", safesearch_answers, None
    ).rr[0] == safesearch_answers[0].getRR("forcesafesearch.google.com")

    reply = req.reply()
    ans = Record.get_answers(
        reply,
        1,
        "forcesafesearch.google.com",
        [*safesearch_answers, *google_answers],
        None,
    ).rr
    assert ans[0] == safesearch_answers[0].getRR("forcesafesearch.google.com")
    assert ans[1] == google_answers[0].getRR("forcesafesearch.google.com")


@handle_test
def test_query():

    answers = [Answer(5, "forcesafesearch.google.com", 300)]

    req = DNSRecord.question("www.google.com", "CNAME")
    reply = req.reply()

    assert Record.query(reply, 5,
                        "www.google.com", req, None).rr[0] == answers[
        0
    ].getRR("www.google.com")


def test_clean_host():
    assert Record.clean_host("www.google.com.") == "www.google.com"
