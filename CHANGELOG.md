# CHANGELOG

## v4-pre-alpha

-   storing enabled domains to decrease load on opendns servers

## v3-pre-alpha

-   moved the whole ip confirmation logic to another repo [dns-ip-confirm](https://github.com/mafazaa-org/dns-ip-confirm)
-   detached from dnsserver package and implemented a whole server
-   switched from zones file to sqlite3 database contains zoneslist, blocklist, and list of keywords for blocking with regex
-   the server uses env variables to determine whether it's a primary or a secondary server

## v2

-   added scripts to automate ip confirmation for opendns

## v1

-   added bash scripts for automation
-   uses two branches for primary and secondary servers
-   switched to opendns
-   added zones for google and youtube's safesearch

## v0

**Initial release**

-   server uses cloudflare as a proxy server
-   everything depends on the dnsserver package
