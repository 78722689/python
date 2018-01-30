from urllib.parse import urlparse
import socket
import logging
import os
import sys

def get_host_ip(url):
    '''
    Return the IP address by giving URL
    '''
    parts = urlparse(url)
    if parts.hostname is not None:
        try:
            host_ip = socket.gethostbyname(parts.hostname)
            return host_ip
        except:
            logger.error('Hostname %s does not find host IP for url %s', parts.hostname, url)

    return ''

def get_hostname(url):
    '''
    Return hostname by giving URL
    '''
    parts = urlparse(url)
    hostname = parts.hostname if parts.hostname is not None else ''

    return hostname

def get_root_path():
    '''
    Return the project root path
    '''
    return os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)).replace('src', '')
    
# To set log format, you can print the log to a file and console, and you can also disable/enable log here
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=get_root_path() + 'output/log.txt',
                    filemode='w'
                    )
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger('')