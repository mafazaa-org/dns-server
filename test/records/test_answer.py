from dns_server.src.records.answer import Answer
from pytest import raises


def test_validation():
    a = Answer(5, "www.test.com.", 400)
    assert a._rtype == 5
    assert a.answer == "www.test.com"
    assert a.ttl == 400

    with raises(ValueError):
        Answer(4303, 34, 400)
