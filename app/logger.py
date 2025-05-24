from fluent.sender import FluentSender
from .constants import ENV_NAME, LEVEL, SERVER_TYPE, LOGGING_HOST, LOGGING_PORT

class Log:
    def __init__(self):
        self.fluentd = FluentSender(f"{LEVEL}-{SERVER_TYPE}{ENV_NAME}", LOGGING_HOST, int(LOGGING_PORT))
    
    def __getattr__(self, attr: str): 
        if attr.startswith("log"):
            if attr.endswith(('reply', 'request')):
                return lambda handler, reply: self.d(f"dnslogger.{attr}", {"data": reply.__str__()},handler)
            return lambda handler, data: self.d(f"dnslogger.{attr}", {"data": data}, handler)
        return super().__getattr__(attr) 
    
    def t(self, event, data, handler = None):
        if ENV_NAME:
            self._log(event,'TRACE', data, handler)
          
    def d(self, event, data, handler = None):
        if ENV_NAME:
            self._log(event,'DEBUG', data, handler)
    
    def i(self, event, data, handler = None):
        self._log(event,'INFO', data, handler) 
        
    def w(self, event, data, handler = None):
        self._log(event,'WARN', data, handler)
    
    def e(self, event, data, handler = None):
        self._log(event,'ERROR', data, handler)
    
    def _log(self, event: str,level: str, data: str | dict, handler = None):
        
        if type(data) == str:
            data = {"msg": data}
    
        if handler:
            data = {**data, "source": self.get_src(handler)}
        data = {**data, "level": level }
        self.fluentd.emit(f"{event}", data)
        
    def get_src(self, handler) -> dict:
       
        return {
            "ip": handler.client_address[0],
            "port": handler.client_address[1]
        }
        

        
logger = Log()