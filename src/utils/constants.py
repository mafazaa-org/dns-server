from .choose import choose
from os import environ

DEFAULT_PORT = 53
UPSTREAMS = ["208.67.222.222", "208.67.220.220"]
LEVELS = ["high", "low"]
BRANCHES = ["dev", "test", "prod"]
ZONES_PATH = "zones"

PROXY_SERVER_TIMEOUT = 5

server = choose(UPSTREAMS, environ["server"], ["primary", "secondary"])
level = choose(LEVELS, environ["level"])
branch = choose(BRANCHES, environ["branch"])
