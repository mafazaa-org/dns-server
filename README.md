# Mafaza DNS Server

A server for blocking adult content, ads, music, movies...etc.

## Install

### Setup on Ubuntu

first clone the repository using the following command

```shell
git clone https://github.com/ahmed-elbehairy7/dns
```

Now customize the upstream server you want to forward to by editing this line in main.py

```python
1 from dnserver import DNSServer
2 from time import sleep
3
4 def main():
5
6     server = DNSServer(upstream = "1.1.1.3") <== RIGHT HERE
7
8     server.start()
```

then run the freePort.sh file to make sure you free port 53 from the systemd-r

```shell
./freePort.sh
```

this script should shutdown the server, when you launch it again, run this command to run the server script

```shell
./run.sh
```

### Content filtering

This is how to do it using opendns, if you want to use another service change the `PRIMARY_SERVER` and `SECONDARY_SERVER` constants in main.py

1. create an `opendns` account
1. go to your [dashboard](https://opendns.com/dashboard)
1. Add the public ip address of the server running the script as a network
1. go to settings, customize it as you like, and congratulations
