from ipaddress import IPv4Address, AddressValueError
from yaml import safe_load
import subprocess
import os


ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))
CONFIG = os.path.join(ROOT, 'config')
CLIENT_DIR = os.path.join(ROOT, 'clients')
BASE_IP = '10.'

def create_config_OLD(ip, client_name):
  with open(os.path.join(CONFIG, 'client_secret.yaml'), 'r', encoding='utf-8') as sf:
    credentials = safe_load(sf)
  
  with open(os.path.join(CONFIG, 'sample.config'), 'r', encoding='utf-8') as f:
    sample = f.read()

  credentials['client_ip'] = ip
  config = sample.format(**credentials)
  
  with open(os.path.join(CLIENT_DIR, f'u{client_name}.conf'), 'w', encoding='utf-8') as wf:
    wf.write(config)

  subprocess.call(['qrencode', '-t', 'ansiutf8', '<', os.path.join(CLIENT_DIR, f'u{client_name}.conf'), '-o', os.path.join(CLIENT_DIR, f'u{client_name}.png')])

  return os.path.exists(CLIENT_DIR, f'u{client_name}.png'), os.path.join(CLIENT_DIR, f'u{client_name}.png')


def create_config(ip, client_name):
  result = subprocess.check_output([os.path.join(CONFIG, 'add_client.sh'), ip, client_name])
  return os.path.exists(os.path.join(CLIENT_DIR, client_name, f'{client_name}.png')), os.path.join(CLIENT_DIR, client_name), result.decode().strip()


def assign_next_ip(existing):
  used = set()
  for ip in existing:
    if not ip: continue
    try:
      ip_obj = IPv4Address(ip)
      used.add(int(ip_obj))
    except AddressValueError:
      continue
  
  for i in range(int(IPv4Address('10.8.0.2')), int(IPv4Address('10.8.255.254'))):
    if i not in used: return str(IPv4Address(i))
  raise ValueError('No available IP addresses left.')
