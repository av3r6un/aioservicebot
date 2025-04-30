from urllib.parse import urlparse
from dotenv import load_dotenv
import sys
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
fp = os.path.join(ROOT, 'config', '.env')
load_dotenv(fp)

def generate_nginx_conf():
  content = """upstream bot-server {
  server              %s fail_timeout=0; 
}

server {
  server_name         %s;
  listen              443 ssl;

  ssl_certificate     /etc/letsencrypt/live/%s/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/%s/privkey.pem;
  include             /etc/options-ssl-nginx.conf;
  ssl_dhparam         /etc/letsencrypt/ssl-dhparams.pem;

  location %s {
    proxy_set_header  Host $http_host;
    proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_redirect    off;
    proxy_buffering   off;
    proxt_pass        http://bot-server;
  }
}
"""
  domain_ = urlparse(os.getenv('SERVER_ADDR')).netloc
  srv_addr_ = f'{os.getenv("WS_HOST")}:{os.getenv("WS_PORT")}'
  location_ = os.getenv('WH_PATH')

  content = content % (srv_addr_, domain_, domain_, domain_, location_)
  with open(os.path.join(ROOT, 'vsb.conf'), 'w', encoding='utf-8') as f:
    f.write(content)
  print("NGINX conf file successfully created!")


def generate_service_file():
  content = """[Unit]
Description=Telegram Async Bot
After=multi-user.target

[Service]
Type=simple
Restart=on-success
WorkingDirectory=%s
ExecStart=%s %s

[Install]
WantedBy=multi-user.target
"""
  start_file = os.path.join(ROOT, 'start.py')
  content = content % (ROOT, sys.executable, start_file)
  with open(os.path.join(ROOT, 'vsb.service'), 'w', encoding='utf-8') as f:
    f.write(content)
  print("Service file successfully created!")


services_files = {
  generate_service_file: os.path.join(ROOT, 'vsb.service'),
  generate_nginx_conf: os.path.join(ROOT, 'vsb.conf')
}
folders = [
  os.path.join(ROOT, 'downloads'), os.path.join(ROOT, 'storage'), os.path.join(ROOT, 'logs')
]
system_directories = {
  os.path.join(ROOT, 'vsb.service'): '/etc/systemd/system/',
  os.path.join(ROOT, 'vsb.conf'): '/etc/nginx/conf.d/',
}

def check_service_files():
  for fn, path in services_files.items():
    if not os.path.exists(path):
      fn()

def create_service_folders():
  for folder in folders:
    if not os.path.exists(folder):
      os.mkdir(folder)

def main():
  create_service_folders()
  check_service_files()


if __name__ == '__main__':
  pass
