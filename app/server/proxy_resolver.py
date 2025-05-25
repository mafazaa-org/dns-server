from dnslib import RCODE
from dnslib.dns import DNSRecord, RR
from dnslib.server import DNSHandler
from app.constants import DEFAULT_PORT
from .resolve import resolve
from traceback import print_exc
from ..logger import logger
from ..records.record import Record

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
        query = {
        "type": _type,
        "qname" : host
                }
        logger.i('req_start', query , handler)
        
        reply = request.reply()

        res_data = self.res_data
        try:
            reply = resolve(request, reply,handler,host,_type,res_data)
        except Exception as e:
            logger.e('resolver_error', {
                            "msg": "exception occured while resolving request",
                            "exception" : e.__str__(),
                            **query
                        }, handler)
            print_exc()
            if not reply.rr:
                reply.header.rcode = getattr(RCODE, "NXDOMAIN")

        unique_rrs = []
        seen = set()
        for rr in reply.rr:
            rr: RR
            # Create a hashable representation for comparison
            rr_key = (rr.rtype, str(rr.rdata))
            print(rr_key)
            if rr_key not in seen:
                seen.add(rr_key)
                unique_rrs.append(rr)

        reply.rr = unique_rrs
        
        for ans in unique_rrs:
            answer = Record.clean_host(ans.rdata.__str__())
            res_data["answers"].append({"answer": answer, "type": ans.rtype})

        logger.i('reply', {**query,**res_data}, handler)
        
        return reply
