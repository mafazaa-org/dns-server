from requests import get
from os import environ

from src.records.block import Block
from src.records.zone import Zone
from src.utils.choose import choose

branch = environ["branch"]
level = environ["level"]

url = (
    lambda file: f"https://raw.githubusercontent.com/mafazaa-org/dns-lists/{branch}/{level}/{file}.json"
)

RecordsClasses = [Block, Zone]


def fetch_records():
    for RecordClass in RecordsClasses:
        data = get(url(RecordClass.file_name)).json()
        RecordClass.initialize(data)


def save_records(): ...
