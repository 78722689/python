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

class MyLogger():
    def __init__(self):
        self.__logger = logging.getLogger('')
        #self.set()

    def debug(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.__logger.critical(msg, *args, **kwargs)

    def set(self, file='', level=1):
        if file == '.' or file == '':
            file = get_root_path() + '/output/log.txt'

        if level == 1:
            level = logging.DEBUG
        elif level == 2:
            level = logging.INFO
        elif level == 3:
            level = logging.WARNING
        elif level == 4:
            level = logging.ERROR
        elif level == 5:
            level = logging.CRITICAL
        else:
            level = logging.DEBUG

        # To set log format, you can print the log to a file and console, and you can also disable/enable log here
        logging.basicConfig(level = level,
                            format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt = '%a, %d %b %Y %H:%M:%S',
                            filename = file,
                            filemode = 'w+'
                            )
        # set up logging to console
        console = logging.StreamHandler()
        console.setLevel(level)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

logger = MyLogger()