# Pam DNS Server

A server for blocking adult content, ads, music, movies...etc.

## Install

### Setup

first clone the repository using the following command

```cmd
git clone https://github.com/ahmed-elbehairy7/dns
```

just install the dnserver module using the following command

```cmd
pip install -r requirements.txt
```

then just run the script src/main.py and test the server

```cmd
python src/main.py
```

and for running the secondary server you just have to add `--secondary` to the command like:

```cmd
python src/main.py --secondary
```

#### Executable

First make sure you have `pyinstaller` installed by running the following command

```cmd
pyinstaller -v
```

for making an executable, you can run the script `build.bat` in your terminal and it will create `dns.exe` in a dist folder

### Content filtering

This is how to do it using opendns, if you want to use another service change the `PRIMARY_SERVER` and `SECONDARY_SERVER` constants in main.py

1. create an `opendns` account
1. go to your [dashboard](https://opendns.com/dashboard)
1. Add the public ip address of the server running the script as a network
1. go to settings, customize it as you like, and congratulations
