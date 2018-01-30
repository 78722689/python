
from Crawler.crawlerfactory import factory
from Crawler.Util.tools import *
from Crawler.Tasks.htmlparser import Parser
from .base import Task
#from gevent.lock import BoundedSemaphore

import urllib3

class HTMLRequest(Task):
    http = urllib3.PoolManager(num_pools=(1024*3), maxsize=1024)
    #http = urllib3.ProxyManager('http://10.144.1.10:8080/', maxsize=1024)
    
    def __init__(self, url, host_ip=''):
        self.__url = self.__format_url(url)
        self.__name = 'HTMLReuest,' + self.__url
        self.__timeout = 5
        self.__host_ip = get_host_ip(self.__url) if host_ip == '' else host_ip

    def __format_url(self, url):
        url = 'http://' + url if url[:4] != 'http' else url
        url = url[:7] + 'www.' + url[7:] if url[7:11] != 'www.' else url

        return url

    @property
    def name(self):
        return self.__name

    @property
    def timeout(self):
        return self.__timeout

    @property
    def job(self):
        return self.__job_handler

    def __byte_2_str(self, data, encoding=[]):
        charsets = ['gbk', 'utf8', 'gb2312', 'ansi']
        for item in encoding + charsets:
            try:
                result = data.decode(item, 'ignore')
                return result
            except:
                logger.error('Decoding content fail.')
        
    def __job_handler(self, id):
        try:
            header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'} #{'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            with HTMLRequest.http.request('GET', self.__url, headers=header, timeout = 20, preload_content=False, decode_content=True) as r:
                logger.debug('Worker-%d, HTTP request status=%s', id, r.status)

                if r.status != 200:
                    logger.debug('Worker-%d, received error-code %d when request to URL %s', id, r.status, self.__url)
                    return

                headers = r.headers['content-type'].split('charset=')
                charset = headers[1] if len(headers) == 2 else []

                task = PageHandler(self.__byte_2_str(r.data,charset), self.__host_ip, self.__url)
                factory.put_task(task)
        except Exception as err:
            logger.error('Worker-%d, request to url(%s) fail, %s', id, self.__url, err)

class PageHandler(Task):
    def __init__(self, html, host, url):
        self.html = html
        self.__name = 'PageHandler'
        self.__host = host
        self.__url = url
        self.__timeout=3

    @property
    def name(self):
        return self.__name

    @property
    def timeout(self):
        return self.__timeout

    @property
    def job(self):
        return self.__job_handler

    def __job_handler(self, id):
        logger.debug('Worker-%d, try to parse %s',id, self.__url)
        parser = Parser(id, self.html, self.__host, self.__url)
        parser.parse()
        logger.debug('Worker-%d, parse %s is done', id, self.__url)

class Injection(Task):
    def __init__(self, url):
        self.__name = 'Injectction'
        self.__url = url
        self.__timeout=3

    @property
    def name(self):
        return self.__name

    @property
    def timeout(self):
        return self.__timeout

    @property
    def job(self):
        return self.__job_handler

    def __job_handler(self, id):
        # Write url to file for further injection analysis
        with open(get_root_path() + 'output/injection_urls.txt', 'a+') as f:
            print(self.__url, file=f)
            f.flush()
