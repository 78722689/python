from urllib.parse import urlparse
import socket

def get_host_ip(url):
    parts = urlparse(url)
    if parts.hostname is not None:
        try:
            host_ip = socket.gethostbyname(parts.hostname)
            print('host_ip = %s' % host_ip)
            return host_ip
        except:
            print('No host IP found in url %s' % url)

    return ''

def get_hostname(url):
    parts = urlparse(url)
    hostname = parts.hostname if parts.hostname is not None else ''

    return hostname
