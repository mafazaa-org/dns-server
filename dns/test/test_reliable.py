from os import popen
from subprocess import Popen

def main():
    server = popen("python src")
    
    with open("test/hosts.txt", "r", encoding="utf-8") as f:
        hosts = f.readlines()
    
    for host in hosts:
        process = Popen(f"nslookup {host.strip()} 127.0.0.1")
        process.wait()
        
    server.close()