from sys import argv

DEFAULT_PORT = 53
ZONES_PATH = "zones"

PROXY_SERVER_TIMEOUT = 5
UPSTREAMS = ["208.67.222.222", "208.67.220.220"]
server = UPSTREAMS[0] if argv[1] == "primary" else UPSTREAMS[1]
