import json
import os
import random
import string
import base64
import re
import argparse
from uuid import uuid4 as rand_uuid

CONFIG_DIR = 'config'
V2RAY_CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')
V2RAY_VMESS_PATH = os.path.join(CONFIG_DIR, 'vmess.txt')
CADDY_CONFIG_PATH = os.path.join(CONFIG_DIR, 'Caddyfile')

# PARAMS
CAMOUFLAGE_PATH_LENGTH = 8

domain = 'fuck.me'
uuid = ''
camouflage_path = ''
alter_id = 64
port_out = 443
port_in = 10086  # normally this should not be modified

randomize = False

def random_init():
    global uuid, camouflage_path
    if randomize:
        uuid = str(rand_uuid())
        camouflage_path = ''.join(random.choice(string.ascii_lowercase)
                                for i in range(CAMOUFLAGE_PATH_LENGTH))
    else:
        with open(V2RAY_CONFIG_PATH) as f:
            j = json.load(f)
            camouflage_path = j['inbounds'][0]['streamSettings']['wsSettings']['path'][1:]
            uuid = j['inbounds'][0]['settings']['clients'][0]['id']
            alter_id = j['inbounds'][0]['settings']['clients'][0]['alterId']
            port_in = j['inbounds'][0]['port']


def modify_v2ray_config():
    with open(V2RAY_CONFIG_PATH) as f:
        j = json.load(f)
        j['inbounds'][0]['streamSettings']['wsSettings']['path'] = '/' + camouflage_path
        j['inbounds'][0]['settings']['clients'][0]['id'] = uuid
        j['inbounds'][0]['settings']['clients'][0]['alterId'] = alter_id
        j['inbounds'][0]['port'] = port_in
    with open(V2RAY_CONFIG_PATH, 'w') as f:
        json.dump(j, f, sort_keys=True, indent=2)


def generate_vmess():
    j = {
        "v": "2",
        "ps": domain,
        "add": domain,
        "port": port_out,
        "id": uuid,
        "aid": alter_id,
        "net": "ws",
        "type": "none",
        "host": domain,
        "path": camouflage_path,
        "tls": "tls"
    }
    s = json.dumps(j)
    vmess = 'vmess://' + base64.b64encode(s.encode('utf8')).decode('utf8')
    with open(V2RAY_VMESS_PATH, 'w+') as f:
        f.write(vmess)
    return vmess


def modify_caddy_config():
    with open(CADDY_CONFIG_PATH) as f:
        content = f.read()
    content = re.sub('path /\w+', f'path /{camouflage_path}', content)
    content = re.sub('reverse_proxy @v2ray_websocket localhost:\d+',
                     f'reverse_proxy @v2ray_websocket localhost:{port_in}', content)
    content = re.sub('# Caddy v2\n.* {',
                     f'# Caddy v2\n{domain}' + ' {', content)
    with open(CADDY_CONFIG_PATH, 'w') as f:
        f.write(content)


if __name__ == "__main__":
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--randomize', dest='randomize', action='store_true', help='randomize params')
    parser.add_argument('-d', '--domain', dest='domain', action='store', help='set domain name')
    args = parser.parse_args()
    randomize = args.randomize
    if args.domain:
        domain = args.domain
        randomize = True

    # main procedure
    random_init()
    modify_v2ray_config()
    generate_vmess()
    modify_caddy_config()
