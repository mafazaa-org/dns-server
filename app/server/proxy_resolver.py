from dnslib import RCODE
from dnslib.dns import DNSRecord
from dnslib.server import DNSHandler
from app.constants import DEFAULT_PORT
from .resolve import resolve
from traceback import print_exc
from ..logger import logger
from ..records.record import Record
from json import dumps

class ProxyResolver:
    
        
    
    def __init__(self):
        self.port = DEFAULT_PORT

    @property
    def res_data(self):
        return {
		"block": False ,
		"block_regex": False,
		"upstream": None,
		"google_regex": False,
		"cache_hit": False,
		"answers": []
	}
        
        
    def resolve(self, request: DNSRecord, handler: DNSHandler):
        _type = request.q.qtype
        host = Record.clean_host(request.q.qname.__str__())
        logger.i('req_start', {
        "type": _type,
        "qname" : host
                }, handler)
        
        reply = request.reply()

        res_data = self.res_data
        try:
            reply = resolve(request, reply,handler,host,_type,res_data)
        except Exception as e:
            logger.e('proxyresolver.error', {
                            "msg": "exception occured while resolving request",
                            "exception" : e
                        }, handler)
            print_exc()
            if not reply.rr:
                reply.header.rcode = getattr(RCODE, "NXDOMAIN")

        
        for ans in reply.rr:
            answer = Record.clean_host(ans.rdata.__str__())
            res_data["answers"].append({"answer": answer, "type": ans.rtype})

        print(dumps({"host": host, "type": _type,**res_data}, indent=4))
        logger.i('reply', res_data, handler)
        
        return reply
