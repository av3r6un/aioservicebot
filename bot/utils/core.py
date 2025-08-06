from ipaddress import IPv4Address, AddressValueError
from zipfile import ZipFile, ZIP_DEFLATED
from yaml import safe_load
import subprocess
import os


ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))
CONFIG = os.path.join(ROOT, 'config')
CLIENT_DIR = os.path.join(ROOT, 'clients')
BASE_IP = '10.'


def create_config(ip, client_name):
  result = subprocess.check_output([os.path.join(CONFIG, 'add_client.sh'), ip, client_name])
  return os.path.exists(os.path.join(CLIENT_DIR, client_name, f'wg_connection.zip')), os.path.join(CLIENT_DIR, client_name)


def make_zip(filepath):
  with ZipFile(f'{filepath}/wg_connection.zip', 'w', ZIP_DEFLATED) as zfile:
    _, uname = os.path.split(filepath)
    user_config = os.path.join(filepath, f'{uname}.conf')
    if not os.path.exists(user_config):
      raise FileNotFoundError(user_config)
    filename = os.path.basename(user_config)
    zfile.write(filepath, arcname=filename)
  return f'{filepath}/wg_connection.zip'

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
