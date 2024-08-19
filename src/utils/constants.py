from .choose import choose
from os import environ

DEFAULT_PORT = 53
UPSTREAMS = ["208.67.222.222", "208.67.220.220"]

PROXY_SERVER_TIMEOUT = 5

server = choose(UPSTREAMS, environ["server"], ["primary", "secondary"])
