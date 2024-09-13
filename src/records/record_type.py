from dnslib import QTYPE

RecordType = (
    QTYPE.A
    | QTYPE.AAAA
    | QTYPE.CAA
    | QTYPE.CNAME
    | QTYPE.DNSKEY
    | QTYPE.MX
    | QTYPE.NAPTR
    | QTYPE.NS
    | QTYPE.PTR
    | QTYPE.RRSIG
    | QTYPE.SOA
    | QTYPE.SRV
    | QTYPE.TXT
    | QTYPE.SPF
    | QTYPE.HTTPS
)
