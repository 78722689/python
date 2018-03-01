
from .base import Task
from .tools import logger, get_root_path

import urllib3

class HttpBase():
    http = urllib3.PoolManager(num_pools=(1024*3), maxsize=1024*5)
    #http = urllib3.ProxyManager('http://10.144.1.10:8080/', maxsize=1024)
    
    def __init__(self):
        pass
        
    def byte_2_str(self, data, encoding=[]):
        charsets = ['gbk', 'utf8', 'gb2312', 'ansi']
        for item in encoding + charsets:
            try:
                result = data.decode(item, 'ignore')
                return result
            except:
                logger.error('Decoding content fail.')
                
class Baidu(HttpBase):
    def __init__(self, keyword, pagenum=1):
        pagenum = pagenum*10
        self.__pagenum = pagenum
        self.__search_url = 'http://www.baidu.com/s?wd=%(keyword)s&rsv_spt=1&rsv_bp=0&ie=utf-8&tn=baiduhome_pg&pn=%(pagenum)d' % vars()

    def request(self, id):
        try:
            #logger.debug('Page-%d, running task (%s)', id, self.__name)
            header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'} #{'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            
            with Baidu.http.request('GET', self.__search_url, headers=header, timeout=20, preload_content=False, decode_content=True) as r:
                logger.debug('Page-%d, HTTP request status=%s', id, r.status)

                if r.status != 200:
                    logger.debug('Page-%d, received error-code %d when request to URL %s', id, r.status, self.__search_url)
                    return

                headers = r.headers['content-type'].split('charset=')
                charset = [headers[1]] if len(headers) == 2 else []

                from .wsecrawlerfactory import factory
                #factory.put_task(Parser(self.byte_2_str(r.data, charset), self.__search_url, self.__pagenum))
                p = Parser(self.byte_2_str(r.data, charset), self.__search_url, self.__pagenum)
                p.parse(self.__pagenum)
        except Exception as err:
            logger.error('Page-%d, request to url(%s) fail, %s', id, self.__search_url, err)

class FetchURL(Task, HttpBase):
    def __init__(self, url, pn):
        self.__url = url
        self.__name = 'FetchURL,' + url
        self.__timeout = 40
        self.__pn = pn
        
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
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}  # {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            with FetchURL.http.request('GET',  self.__url, headers=header, timeout=self.__timeout, redirect=False, preload_content=False, decode_content=True) as resp:
                url = resp.headers.get('location')
                logger.info('Worker-%d, %s real url is %s',id, self.__url, resp.headers.get('location'))
                from .wsecrawlerfactory import factory
                factory.put_task(Output(url, self.__pn))
        except Exception as err:
            logger.error('Worker-%d, request to url(%s) fail, %s', id,  self.__url, err)

    def done(self):
        pass

class Output(Task):
    file = open(get_root_path()+'/output/result.txt', 'w+')

    def __init__(self, url, pn):
        self.__url = url
        self.__name = 'Output'
        self.__pn = pn

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
        print(self.__url, file=Output.file)
        Output.file.flush()
        self.done()

    def done(self):
        from .wsecrawlerfactory import factory
        factory.put_message({'page': self.__pn / 10, 'count': -1})

class Parser():
    def __init__(self, html, url, pn):
        self.__html = html
        self.__name = 'Parser,' + url
        self.__timeout = 10
        self.__pagenumber= pn

    def done(self):
        from .wsecrawlerfactory import factory
        factory.put_message({'page': self.__pagenumber / 10, 'count': 0})

    def parse(self, id):
        logger.debug('Parser-%d, Parser entry', id)
        from bs4 import BeautifulSoup as bs

        soup = bs(self.__html, 'lxml')
        pn = soup.find_all("span", "pc")
        if len(pn) <= 0:
            logger.error('Did not find the page count in page %d, skip it', self.__name, self.__pagenumber)
            self.done()
            return
        if (self.__pagenumber/10) > 10 and pn[0].get_text() == '1':
            logger.warn('%s Page %d do not have the content, skip it.', self.__name, self.__pagenumber)
            self.done()
            return

        links = soup.find_all('a')
        i=0
        from .wsecrawlerfactory import factory
        for link in links:
            if link.get('data-click') is None or link.get('data-click') == '': continue
            target_url = link.get('href')
            if target_url is not None and 'link?url=' in target_url:
                logger.debug('Found link %s', target_url)

                factory.put_task(FetchURL(target_url, self.__pagenumber))

                i+=1
        factory.put_message({'page':self.__pagenumber/10, 'count':i})
        logger.debug('Found %d links', i)