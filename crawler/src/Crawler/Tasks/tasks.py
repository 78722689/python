import time
from Crawler.Tasks.base import Task
from Crawler.crawler import crawler_singleton
from Crawler.HTMLHandler.htmlparser import Parser

import urllib3
urllib3.disable_warnings()

class HTMLRequest(Task):
    http = urllib3.PoolManager()

    def __init__(self, url):
        self.__url = url
        self.__name = 'HTMLReuest'

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
        try:
            header = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            with HTMLRequest.http.request('GET', self.__url, headers=header, timeout = 10, preload_content=False, decode_content=True) as r:

                task = PageHandler(r.data.decode('utf-8', 'ignore'))
                crawler_singleton.put_task(task)
        except Exception as err:
            print('Request to url(%s) fail, %s' % (self.__url, err))

class PageHandler(Task):
    def __init__(self, html):
        self.html = html
        self.__name = 'PageHandler'

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
        parser = Parser(self.html)
        parser.parse()
        #with open('E:\Programing\python\python\crawler\output\page.html', 'w+') as f:
        #    print(self.html)
        #    f.write(str(self.html))
        #    f.flush()

        #time.sleep(20)


