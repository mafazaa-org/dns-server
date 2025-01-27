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

## Configuration Documentaion

### Environment Variables

#### Overview
The .env file is used to set environment variables that configure the operation of the application. These variables are used to define settings such as server addresses, database connections, and operational levels, which can be accessed throughout the application to maintain flexibility and ease of deployment.

#### Environment Variables

##### UPSTREAM
Specifies the upstream DNS server to which DNS queries are forwarded if the local server cannot resolve them. Locally, it is high-dns.mafazaa.com or low-dns.mafazaa.com but it is OpenDNS in production phase. An exanple for that is

    UPSTREAM=high-dns.mafazaa.com

This allows the application to leverage external DNS servers for queries that it does not handle directly, improving responsiveness and capability.

##### PUBLIC_DNS
The IP address of a public DNS server that can be used for instead of OpenDNS since sending unlimited requests to OpenDNS requires subscription. The example below shows the PUBLIC_DNS (8.8.8.8) which is Google's Public DNS Server. The code below is an example of identifying an IP address for public DNS server

    PUBLIC_DNS=8.8.8.8

When we this code is executed, the device requests from Google whether a specific IP address exists. If so, the device checks if that IP address will be blocked or not.

##### DB_ADDR
The URL of the database that the application will connect to, which is a large databese in production phase.

    DB_ADDR=http://localhost:1212

This variable specifies where the application will find the database server, enabling support for features that involve persistent storage or caching of data.

##### LEVEL
Represents security level of the server. Low level DNS only blocks Pornography, and inappropriate cartoons and comics websites while high level DNS bloks other websites like Netflix and spotify along with the those mentioned bafore.

    LEVEL=high

It's purpose is to ensure that specified IP addresses are blocked.
            
##### REDIS_PORT
The port used for establishing a connection to the Redis database.

    REDIS_PORT=6379

This specifies the port through which the application communicates with Redis, a commonly used in-memory store for caching and rapid data retrieval.

##### REDIS_HOST
The hostname or IP address of the Redis database server.

    REDIS_HOST=localhost

This variable allows the application to know where the Redis service is hosted, facilitating connections to it for data retrieval and storage.

##### SERVER_HOSTNAME
The hostname of the DNS server itself.

    SERVER_HOSTNAME=localhost

This may be used in logging, providing information about the server’s identity in various messages and responses, or possibly in responses to queries.

#### Usage in Application
These environment variables are loaded into the application at runtime using the dotenv library. Here's how they typically work in context:

Initialization: At the start of the application, load_dotenv() is called to import these variables, making them accessible via os.getenv().

Configuration: The application will use these configurations to set up connections (to Redis, to a database) and to configure its logging and behavior based on the provided values.

Environmental Flexibility: Using environment variables allows you to change configurations easily without altering the source code, facilitating different setups for development, testing, and production environments.
