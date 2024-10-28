#!/bin/bash

git clone https://github.com/xLLMA/OllamaServer.git &&
cd OllamaServer &&
python3 pull.py &&
read -p "Enter the desired OLLAMA repository name (e.g., orca-mini): " repo_name &&
sudo apt update &&
sudo apt install nginx -y &&
curl https://ollama.ai/install.sh | sh &&
OLLAMA_HOST=0.0.0.0:1434 &&
service ollama start &&
ollama pull $repo_name &&
IP=$(curl -s4 ifconfig.me); echo "server { listen $IP:11434; server_name _; location / { proxy_pass http://127.0.0.1:11434; proxy_set_header Host \$host; proxy_set_header X-Real-IP \$remote_addr; }}" | sudo tee /etc/nginx/sites-available/ollma > /dev/null &&
sudo ln -s /etc/nginx/sites-available/ollma /etc/nginx/sites-enabled/ &&
sudo nginx -t &&
sudo systemctl restart nginx &&
echo "Ollama installation and configuration completed." &&
echo "API is available at http://$IP:11434"
