from ipaddress import IPv4Address, AddressValueError
from yaml import safe_load
import subprocess
import os


ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))
CONFIG = os.path.join(ROOT, 'config')
CLIENT_DIR = os.path.join(ROOT, 'clients')
BASE_IP = '10.'

def create_config(ip, client_name):
  with open(os.path.join(CONFIG, 'client_secret.yaml'), 'r', encoding='utf-8') as sf:
    credentials = safe_load(sf)
  
  with open(os.path.join(CONFIG, 'sample.config'), 'r', encoding='utf-8') as f:
    sample = f.read()

  # credentials['private_key'] = subprocess.check_output(['wg', 'genkey']).decode().strip()
  credentials['private_key'] = 'sBSFaL2f9mH5BWvRfypM3IfBGoseBtC8zGrB63Te0X8='
  credentials['client_ip'] = ip
  config = sample.format(**credentials)
  
  with open(os.path.join(CLIENT_DIR, f'u{client_name}.conf'), 'w', encoding='utf-8') as wf:
    wf.write(config)
  
  return os.path.join(CLIENT_DIR, f'u{client_name}.conf')


def assign_next_ip(existing):
  used = set()
  for ip in existing:
    if not ip: continue
    try:
      ip_obj = IPv4Address(ip)
      used.add(int(ip_obj))
    except AddressValueError:
      continue
  
  for i in range(int(IPv4Address('10.0.0.2')), int(IPv4Address('10.255.255.254'))):
    if i not in used: return str(IPv4Address(i))
  raise ValueError('No available IP addresses left.')
