from imaplib import IMAP4_SSL
from email import message_from_bytes
from re import search
from getpass import getpass
from os import popen

def main():
    server = input("Enter mail server: ")
    print("please enter the credentials to login to your email and read the inbox")
    email_address = input("Email: ")
    password = getpass("password: ")
    ip_address = input("Server Ip Address(You should be running this script from this ip address): ")
    
    link = None
    
    imap = IMAP4_SSL(server)
    
    imap.login(email_address, password)
    
    imap.select("Inbox")

    _, msgnums = imap.search(None, "ALL")
    
    for msgnum in msgnums[0].split():
        _, data = imap.fetch(msgnum, "(RFC822)")
        
        message = message_from_bytes(data[0][1])
        
        if message.get("subject") != "[OpenDNS] Verify your IP address":
            continue
        
        for part in message.walk():
            if part.get_content_type() != "text/plain":
                continue
            
            string = part.as_string()
            
            if search(ip_address, string) == None:
                continue
            
            link = (search("https://dashboard-ipv4.opendns.com/n/.+", string).group().strip())
            
    print("Please enter the credentials to login to your openDNS account")
    popen(cmd= f"node ip/index.js {link} {input("openDNS email: ")} {getpass("openDNS password: ")}")
                
    imap.close()
    
    
if __name__ == '__main__':
    main()