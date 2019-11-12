import socket
import time
import configparser

def internet(host="8.8.8.8", port=53, timeout=3, cmd=''):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  print(host)
  global timeout_sleep
  global DEFAULT_SLEEP
  error_count = 0
  while error_count < 10:
    try:
      socket.setdefaulttimeout(timeout)
      socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
      if timeout_sleep < 30:
        timeout_sleep += DEFAULT_SLEEP
      return True
    except socket.error as ex:
      timeout_sleep = DEFAULT_SLEEP # reset sleep timeout
      error_count += 1
      time.sleep(1)

  if error_count >= 10:
    os.system(cmd)
    print('Error: 10 times without access to', host, '-- reconnecting...')

# Setup global variables
DEFAULT_SLEEP = 5             # constant
timeout_sleep = DEFAULT_SLEEP # timeout to check internet -- increases as connection becomes stable

# Get ip configuration
config = configparser.ConfigParser()
try:
  config.read('./config.txt')
  general = config['general']
except KeyError as ex:
  config['general'] = {}
  general = config['general']



# try to get config, fails to default case
options = {}
options['host'] = general.get('host', '8.8.8.8')
options['port'] = general.get('port', 53)
options['timeout'] = general.get('timeout', 3)
options['cmd'] = general.get('cmd', 'echo \'define cmd in config.txt\'')

# Runs forever
while True:
  internet(options['host'], options['port'], options['timeout'], options['cmd'])
  time.sleep(timeout_sleep)
