# Install dependencies
sudo apt update
sudo apt install -y git python3 curl

# Install docker
install_docker() {
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
}

# Install docker-compose
install_docker_compose() {
    sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
}

# Install bbr script
install_bbr() {
    wget -N "https://github.000060000.xyz/tcp.sh" && chmod +x tcp.sh
}

[[ -f "/usr/bin/docker" ]] || install_docker
[[ -f "/usr/local/bin/docker-compose" ]] || install_docker_compose
git clone https://github.com/xunge2020/v2ray-caddy-docker
install_bbr

echo -e '\n\n========================================'
echo -e     '|  Now follow the instructions below   |'
echo -e     '========================================\n'
echo -e 'cd v2ray-caddy-docker'
echo -e 'python3 go.py --domain <your_domain>'
echo -e 'docker-compose up -d'
echo -e 'cat config/vmess.txt'
echo -e './tcp.sh  # turn on bbr (optional)'
echo -e
