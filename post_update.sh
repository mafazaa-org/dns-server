sudo pip3 install -r requirements.txt --break-system-packages

# Clean old

sudo pip3 uninstall dnserver

# clean prepare

sudo apt remove python3-pip -y

sudo apt autoremove -y

sudo apt autoclean -y

sudo apt clean -y

sudo apt-get autoremove -y

sudo apt-get autoclean -y

sudo apt-get clean -y