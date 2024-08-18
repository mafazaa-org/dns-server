from re import sub
from dataclasses import dataclass
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

RecordType = Literal[
    'A', 'AAAA', 'CAA', 'CNAME', 'DNSKEY', 'MX', 'NAPTR', 'NS', 'PTR', 'RRSIG', 'SOA', 'SRV', 'TXT', 'SPF'
]
RECORD_TYPES = RecordType.__args__ 


@dataclass
class Zone:
    host : str
    type : RecordType
    answer: str | list[str | int]
    
    @classmethod
    def from_json(cls, index: int, data):
        if not isinstance(data, dict) or data.keys() != {'host', 'type', 'answer'}:
            raise ValueError(
                f'Zone {index} is not a valid dict, must have keys "host", "type" and "answer", got {data!r}'
            )

        host = data['host']
        if not isinstance(host, str):
            raise ValueError(f'Zone {index} is invalid, "host" must be string, got {data!r}')

        type_ = data['type']
        if type_ not in RECORD_TYPES:
            raise ValueError(f'Zone {index} is invalid, "type" must be one of {", ".join(RECORD_TYPES)}, got {data!r}')

        answer = data['answer']
        if isinstance(answer, str):
            answer = sub(r'\s*\r?\n', '', answer)
        elif not isinstance(answer, list) or not all(isinstance(x, (str, int)) for x in answer):
            raise ValueError(
                f'Zone {index} is invalid, "answer" must be a string or list of strings and ints, got {data!r}'
            )

        return cls(host, type_, answer)