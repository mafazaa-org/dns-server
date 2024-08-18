from json import load, dump
from dns.src.local.record import Record, load_records, save_records
from dns.src.local.zone import Zone

test_json = "test/local/test_record.json"


def main():
    test_load()


def test_load():
    l = [{"host": "example.com", "type": "A", "answer": "1.2.3.4"}]
    dump(l, open(test_json, "w"))

    load_records(test_json)
    zone = Zone(l[0]["host"], l[0]["type"], l[0]["answer"])

    assert Record.zones == [zone]
    assert Record.records[0]._rname == Record(zone)._rname


if __name__ == "__main__":
    main()
