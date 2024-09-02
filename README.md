# Mafaza DNS Server

A server for blocking adult content, ads, music, movies...etc.

## Install

### setup

first, see the [dns-init](https://github.com/mafazaa-org/dns-init) repository to setup the server

the `define.sh` script should automaticly clone all dns-server repos to the server, if it didn't for some reason, run the `update.sh` script from the dns-init repository manually

### ip confirmation

second, make sure to confirm the ip address of the server you are using, for more details on how to do it, check the [dns-ip-confirm](https://github.com/mafazaa-org/dns-ip-confirm) repository on how to do that programaticly

> this step runs only once if you're using static ip addresses

### run the server

Finally: to run the server, run the following command, this should run the server in a tmux session, if you want to check on it you can run `tmux attach`. to detach from tmux without losing the running server press `ctrl + B` then `release` then press `D`

```shell
./run.sh
```

### monitoring

monitoring the server from the outside is a must, and we also offer monitoring from the inside of the server, the [dns-check](https://github.com/mafazaa-org/dns-check) repository contains the scripts and logic responsible for monitoring the server from the inside and run the server automaticly if the server caught offline

### Updating

if you used the dns-init scripts a crontab job should be automaticly added to update the server every certain period of time

### Content filtering

This is how to do it using opendns:

1. Go to [opendns website](https://opendns.com)
1. Choose the consumer option not the enterprise one
1. choose openDNS Home and sign up for a free account
1. go to your [dashboard](https://opendns.com/dashboard) and login if needed
1. Add the public ip address of the server running the script as a network
1. go to settings, customize content-filtering as you like
1. Congratulations!
