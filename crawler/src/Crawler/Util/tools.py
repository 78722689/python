from urllib.parse import urlparse
import socket
import logging as logger


# To set log format, you can print the log to a file and console, and you can also disable/enable log here
logger.basicConfig(level=logger.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/mnt/python/crawler/output/log.txt', #'E:\Programing\python\output\log.log'
                    filemode='w'
                    )
# set up logging to console
console = logger.StreamHandler()
console.setLevel(logger.DEBUG)
# set a format which is simpler for console use
formatter = logger.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logger.getLogger('').addHandler(console)

def get_host_ip(url):
    parts = urlparse(url)
    if parts.hostname is not None:
        try:
            host_ip = socket.gethostbyname(parts.hostname)
            return host_ip
        except:
            logger.error('Hostname %s does not find host IP for url %s', parts.hostname, url)

    return ''

def get_hostname(url):
    parts = urlparse(url)
    hostname = parts.hostname if parts.hostname is not None else ''

    return hostname
