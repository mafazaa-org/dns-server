echo 
echo uncomment DNS and DNSStubListener and change them to {your.Dns.Server.ip} and no respectively
echo 
echo ok
read

sudo nano /etc/systemd/resolved.conf

echo 
echo assuming you did it we are creating a soft link now!

sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf

echo
echo congratulations, now we are going to shutdown the system
echo 
read

sudo shutdown