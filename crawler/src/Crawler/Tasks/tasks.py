import time
#from Crawler.Tasks.base import Task

from Crawler.crawler import crawler_singleton
from Crawler.Util.tools import *
from Crawler.Tasks.htmlparser import Parser
from .base import Task
from gevent.lock import BoundedSemaphore

import urllib3

class HTMLRequest(Task):
    http = urllib3.PoolManager()
    #http = urllib3.ProxyManager('http://10.144.1.10:8080/', maxsize=1024)
    
    # Save the URLs which have been accessed in the past
    # format{url:True}
    requested_urls = {}

    sem = BoundedSemaphore(1)
    
    def __init__(self, url, host_ip=''):
        self.__url = url
        self.__name = 'HTMLReuest'
        self.__timeout = 20
        self.__host_ip = get_host_ip(self.__url) if host_ip == '' else host_ip

    #def __get_host_ip(self):
    #    parts = urlparse(self.__url)
    #    if parts.hostname is not None:
    #        try:
    #            host_ip = socket.gethostbyname(parts.hostname)
    #            return host_ip
    #        except:
    #            print('No host IP found in url %s' % self.__url)
    #            pass

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
                print('Decoding content fail.')
        
    def __job_handler(self, id):

        #HTMLRequest.sem.acquire()

        # If url has been accessed, skip it.
        if HTMLRequest.requested_urls.get(self.__url) is not None: return
        # If no requested in the past, saving the URL so that to prevent the access in multi-times
        HTMLRequest.requested_urls.update({self.__url:True})

        # Test code
        with open('E:\Programing\python\output\\requested_urls.txt', 'a+') as f:
            print(self.__url, file=f)
            f.flush()
        #HTMLRequest.sem.release()

        try:
            header = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            with HTMLRequest.http.request('GET', self.__url, headers=header, timeout = 20, redirect=False, preload_content=False, decode_content=True) as r:
                print('status=%s' % r.status)
                if r.status != 200:
                    print('Received error-code %d when request to URL %s' % (r.status, self.__url))
                    return
                
                task = PageHandler(self.__byte_2_str(r.data, [r.headers['content-type'].split('charset=')[1]]), self.__host_ip, self.__url)
                crawler_singleton.put_task(task)
        except Exception as err:
            print('Request to url(%s) fail, %s' % (self.__url, err))


class PageHandler(Task):
    def __init__(self, html, host, url):
        self.html = html
        self.__name = 'PageHandler'
        self.__host = host
        self.__url = url

    @property
    def name(self):
        return self.__name

    @property
    def timeout(self):
        pass

    @property
    def job(self):
        return self.__job_handler

    def __job_handler(self, id):
        print('In pagehandler===========')
        parser = Parser(self.html, self.__host, self.__url)
        parser.parse()

class Injection(Task):
    # Save the injection URLs in dictionary so that it will not be written to file twice.
    # {url:True}
    all_inject_target_urls = {}

    sem = BoundedSemaphore(1)

    def __init__(self, url):
        self.__name = 'Injectction'
        self.__url = url

    @property
    def name(self):
        return self.__name

    @property
    def timeout(self):
        pass

    @property
    def job(self):
        return self.__job_handler

    def __job_handler(self, id):
        if Injection.all_inject_target_urls.get(self.__url) is not None: return

        # Write url to file for further injection analysis
        with open('E:\Programing\python\output\injection_urls.txt', 'a+') as f:
            print(self.__url, file=f)
            f.flush()

        Injection.all_inject_target_urls.update({self.__url:True})
