sudo apt update

sudo apt install chromium-browser nodejs npm -y

cd ip && npm install && cd ..

python3 ip/ip_confirm.py

sudo apt remove nodejs npm chromium-browser -y

sudo apt autoremove -y

sudo apt autoclean -y

sudo apt clean -y

sudo apt-get autoremove -y

sudo apt-get autoclean -y

sudo apt-get clean -y