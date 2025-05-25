from fluent.sender import FluentSender
from .constants import LOG_LEVEL, LOG_HOST, LOG_PORT, LOG_INDEX

class Log:
    
    levels = ["t", "d", "i", "w", "e"]
    
    def __init__(self):
        self.fluentd = FluentSender(LOG_INDEX, LOG_HOST, int(LOG_PORT))
        self.level = LOG_LEVEL
        i = self.levels.index(LOG_LEVEL)
        self.disabled = self.levels[:i]
        for level in self.disabled:
            setattr(self, level, lambda self, *args, **kwargs: None)
    
    def __getattr__(self, attr: str): 
        if attr.startswith("log"):
            
            if attr.endswith(('reply', 'request')):
                return lambda handler, reply: self.d(f"dnslogger.{attr}", {"data": reply.__str__()},handler)
            if attr == "log_error":
                return lambda handler, e: self.e(f"dnslogger.{attr}", {"e": e.__str__()}, handler)
            return lambda handler, data: self.d(f"dnslogger.{attr}", {"data": data.__str__()}, handler)


        return super().__getattr__(attr) 
    
    def t(self, event, data, handler = None):
        self._log(event,'TRACE', data, handler)
          
    def d(self, event, data, handler = None):
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
        try:
            self.fluentd.emit(f"{event}", data)
        except:
            pass
        
    def get_src(self, handler) -> dict:
       
        return {
            "ip": handler.client_address[0],
            "port": handler.client_address[1]
        }
        

        
logger = Log()