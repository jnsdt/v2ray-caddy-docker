## V2Ray Caddy Docker

### Installation

```
wget -N --no-check-certificate https://raw.githubusercontent.com/xunge2020/v2ray-caddy-docker/master/install.sh
chmod +x install.sh
./install.sh
```

Follow the instructions to complete

### Update

To update v2ray-core simply run

```
docker pull v2fly/v2fly-core
docker-compose up --force-recreate --build -d
docker image prune -f
```
