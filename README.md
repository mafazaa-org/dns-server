# Mafaza DNS Server

A server for blocking adult content, ads, music, movies...etc.

## Install

### Setup on Ubuntu

first clone the repository using the following command

```shell
git clone -b primary https://github.com/ahmed-elbehairy7/dns
```

the branch argument for choosing between primary server and secondary server, this automaticly assign upstreams to primary and secondary opendns servers! also, the update.sh script correctly fetch from primary of secondary branch

First of all, you have to add the execute permission to files by the following command

```shell
chmod +x *
```

then run the freePort.sh file to make sure you free port 53 from the systemd-r, this script should shutdown the server, so be ready for that

```shell
./freePort.sh
```

If you are not using opendns then skip this step, if you do, make sure you completed [content filtering setup](#content-filtering)

```shell
./confirmIp.sh

./cleanConfirmIp.sh
```

The last step to setup your dns server is to run this command to install dependencies and prepare the server for running the server script

```shell
./prepare.sh

./cleanPrepare.sh
```

Finally: to run the server, run the following command, this should run the server in a tmux session, if you want to check on it you can run `tmux attach`. to detach from tmux without losing the running server press `ctrl + B` then `release` then press `D`

```shell
./run.sh
```

### Updating

The script updateDev.bat is for updating primary and secondary branches from dev so don't come close to it unless you need to! the script you're looking for is the `update.sh` script

```shell
./update.sh
```

### Content filtering

This is how to do it using opendns:

1. Go to [opendns website](https://opendns.com)
1. Choose the consumer option not the enterprise one
1. choose openDNS Home and sign up for a free account
1. go to your [dashboard](https://opendns.com/dashboard) and login if needed
1. Add the public ip address of the server running the script as a network
1. go to settings, customize content-filtering as you like
1. Congratulations!
