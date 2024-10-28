#!/bin/bash

# Update the system and install required packages
echo "Updating system and installing necessary packages..."
sudo apt update -y && sudo apt install nginx curl git -y
git clone https://github.com/xLLMA/OllamaServer&&cd OllamaServer
# permission 
chmod +x install.sh
# run install file
bash install.sh
