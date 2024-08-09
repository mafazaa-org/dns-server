DEFAULT_PORT = 53
class DnsServer():
    def __init__(self, upstream : str) -> None:
        self.upstream = upstream
        

    def start(self):
        print('starting DNS server on port %d, upstream DNS server "%s"', DEFAULT_PORT, self.upstream)
        