#!/bin/bash

# Check for root permissions
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi


echo "Running pull.py to let user select a repository..."
python3 pull.py

# Check if repo.txt was created and read the repo_name
if [[ -f "repo.txt" ]]; then
    repo_name=$(<repo.txt)
    echo "Repository name retrieved: $repo_name"
else
    echo "Error: repo.txt not found. Exiting..."
    exit 1
fi

# Update the system and install required packages
echo "Updating system and installing necessary packages..."
sudo apt update -y && sudo apt install nginx curl git -y

# Check if Ollama is installed, if not, install it
if ! command -v ollama &> /dev/null
then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed."
fi

# Set OLLAMA to listen on all interfaces (0.0.0.0) at port 1434
export OLLAMA_HOST="0.0.0.0:1434"
echo "OLLAMA_HOST set to $OLLAMA_HOST"

# Start Ollama service
echo "Starting Ollama service..."
sudo service ollama start

# Pull the desired repository
echo "Pulling repository: $repo_name ..."
ollama pull "$repo_name"

# Get the public IP of the server
IP=$(curl -s ifconfig.me)
if [[ -z "$IP" ]]; then
    echo "Error fetching public IP. Exiting..."
    exit 1
fi
echo "Public IP: $IP"

# Nginx configuration for proxying Ollama API
nginx_conf="server {
    listen $IP:11434;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:1434;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}"

# Write Nginx configuration to appropriate file
echo "Configuring Nginx for Ollama API..."
echo "$nginx_conf" | sudo tee /etc/nginx/sites-available/ollama > /dev/null

# Enable the new configuration
sudo ln -s /etc/nginx/sites-available/ollama /etc/nginx/sites-enabled/

# Test Nginx configuration for any errors
sudo nginx -t
if [[ $? -ne 0 ]]; then
    echo "Nginx configuration test failed. Exiting..."
    exit 1
fi

# Restart Nginx to apply the new configuration
echo "Restarting Nginx..."
sudo systemctl restart nginx

# Final message
echo "Ollama installation and configuration completed."
echo "API is available at http://$IP:11434"
