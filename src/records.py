import sys
from zone import Zone
from dataclasses import dataclass

@dataclass
class Records:
    zones: list[Zone]
    
    def load_records(zones_file: str) -> Records:
        data = parse_toml(zones_file)
        
        zones = data['zones']
        
        if not isinstance(zones, list):
            raise ValueError(f"Zones must be a list, not {type(zones).__name__}")
        return Records([Zone.from_raw(i, zone) for i, zone in enumerate(zones, start=1)])
        
    
    def parse_toml(zones_file : str):
        if sys.version_info >= (3, 11):
            import tomllib as toml_
        else:
            import tomii as tomi_
        
        with open(zones_file, 'rb') as rf:
            return toml_.load(rf)