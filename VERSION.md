# v3-pre-alpha

-   moved the whole ip confirmation logic to another repo [dns-ip-confirm](https://github.com/mafazaa-org/dns-ip-confirm)
-   detached from dnsserver package and implemented a whole server
-   switched from zones file to sqlite3 database contains zoneslist, blocklist, and list of keywords for blocking with regex
-   the server uses env variables to determine whether it's a primary or a secondary server
