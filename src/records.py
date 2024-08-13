import sys
from zone import Zone
from dataclasses import dataclass
from json import load, dump
    
@dataclass
class Records:
    zones: list[Zone]
    
def load_records(zones_file: str) -> Records:
    with open(zones_file, "r") as rf:
        data = load(rf)
    
    zones = data
    
    if not isinstance(zones, list):
        raise ValueError(f"Zones must be a list, not {type(zones).__name__}")
    return Records([Zone.from_raw(i, zone) for i, zone in enumerate(zones, start=1)])
    

def save_records(zones_file: str, records : Records):       
    with open(zones_file, 'w') as wf:
        dump( [{"host" : zone.host, "type" : zone.type, "answer" : zone.answer} for zone in records.zones], wf)
        