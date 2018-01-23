import time
#from Crawler.Tasks.base import Task

from Crawler.crawler import crawler_singleton
from Crawler.Util.tools import *
from Crawler.Tasks.htmlparser import Parser
from .base import Task
from gevent.lock import BoundedSemaphore

import urllib3

class HTMLRequest(Task):
    http = urllib3.PoolManager(num_pools=(1024))
    #http = urllib3.ProxyManager('http://10.144.1.10:8080/', maxsize=1024)
    
    # Save the URLs which have been accessed in the past
    # format{url:True}
    requested_urls = {}

    #sem = BoundedSemaphore(1)
    
    def __init__(self, url, host_ip=''):
        self.__url = url
        self.__name = 'HTMLReuest,' + url
        self.__timeout = 5
        self.__host_ip = get_host_ip(self.__url) if host_ip == '' else host_ip

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

        #HTMLRequest.sem.acquire()

        # If url has been accessed, skip it.
        #if HTMLRequest.requested_urls.get(self.__url) is not None: return
        # If no requested in the past, saving the URL so that to prevent the access in multi-times
        #HTMLRequest.requested_urls.update({self.__url:True})

        # Test code
        #with ('E:\Programing\python\output\\requested_urls.txt', 'a+') as f:
        #    print(self.__url, file=f)
        #    f.flush()
        #HTMLRequest.sem.release()
        #logger.debug('Worker-%d, try to request %s', id, self.__url)

        try:
            header = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            with HTMLRequest.http.request('GET', self.__url, headers=header, timeout = 20, redirect=False, preload_content=False, decode_content=True) as r:
                logger.debug('Worker-%d, HTTP request status=%s', id, r.status)

                if r.status != 200:
                    logger.debug('Worker-%d, received error-code %d when request to URL %s', id, r.status, self.__url)
                    return
                
                task = PageHandler(self.__byte_2_str(r.data, [r.headers['content-type'].split('charset=')[1]]), self.__host_ip, self.__url)
                crawler_singleton.put_task(task)
        except Exception as err:
            logger.debug('Worker-%d, request to url(%s) fail, %s', id, self.__url, err)

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
        #logger.debug('Worker-%d, try to parse %s',id, self.__url)
        parser = Parser(id, self.html, self.__host, self.__url)
        parser.parse()
        #logger.debug('Worker-%d, parse %s is done', id, self.__url)

class Injection(Task):
    # Save the injection URLs in dictionary so that it will not be written to file twice.
    # {url:True}
    all_inject_target_urls = {}

    sem = BoundedSemaphore(1)

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
        if Injection.all_inject_target_urls.get(self.__url) is not None: return

        # Write url to file for further injection analysis
        #with open('E:\Programing\python\output\injection_urls.txt', 'a+') as f:#open('/mnt/python/crawler/output/injection_urls.txt', 'a+') as f:
        #    print(self.__url, file=f)
        #    f.flush()

        Injection.all_inject_target_urls.update({self.__url:True})
