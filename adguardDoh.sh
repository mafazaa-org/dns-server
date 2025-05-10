wget https://github.com/AdguardTeam/dnsproxy/releases/download/v0.75.3/dnsproxy-linux-amd64-v0.75.3.tar.gz

tar -xvzf dnsproxy-linux-amd64-v0.75.3.tar.gz

sudo apt install certbot -y

./dnsproxy -l 0.0.0.0 --tls-port=853 --https-port=443 --http3 --tls-crt=/etc/letsencrypt/live/high-dns.mafazaa.com/fullchain.pem --tls-key=/etc/letsencrypt/live/high-dns.mafazaa.com/privkey.pem -u 127.0.0.1 -p 0 -cache --https-server-name=high-dns.mafazaa.com