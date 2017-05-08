sudo apt-get update
sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb
sudo apt-get install -f
sudo apt-get install xvfb unzip
wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
sudo apt-get install python-pip
sudo pip install pyvirtualdisplay selenium pandas boto 
## if needed: sudo rm /var/cache/apt/archives/lock sudo rm /var/lib/dpkg/lock sudo rm /var/lib/apt/lists/lock