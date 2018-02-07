
from .base import Task
from .tools import logger, get_root_path

import urllib3

class HttpBase():
    http = urllib3.PoolManager(num_pools=(1024*3), maxsize=1024)
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
                
class Baidu(Task, HttpBase):
    def __init__(self, keyword, pagenum=1):
        pagenum = pagenum*10+1
        self.__search_url = 'http://www.baidu.com/s?wd=%(keyword)s&rsv_spt=1&rsv_bp=0&ie=utf-8&tn=baiduhome_pg&pn=%(pagenum)d' % vars()
        self.__name = 'Baidu,' + self.__search_url
        self.__timeout = 20

    def __format_url(self, url):
        url = 'http://' + url if url[:4] != 'http' else url

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
        
    def __job_handler(self, id):
        try:
            logger.debug('Worker-%d, running task (%s)', id, self.__name)
            header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'} #{'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            
            with Baidu.http.request('GET', self.__search_url, headers=header, timeout = self.__timeout, preload_content=False, decode_content=True) as r:
                logger.debug('Worker-%d, HTTP request status=%s', id, r.status)

                if r.status != 200:
                    logger.debug('Worker-%d, received error-code %d when request to URL %s', id, r.status, self.__url)
                    return

                headers = r.headers['content-type'].split('charset=')
                charset = [headers[1]] if len(headers) == 2 else []

                from .wsecrawlerfactory import factory
                factory.put_task(Parser(self.byte_2_str(r.data, charset)))
        except Exception as err:
            logger.error('Worker-%d, request to url(%s) fail, %s', id, self.__search_url, err)

class FetchURL(Task, HttpBase):
    def __init__(self, url):
        self.__url = url
        self.__name = 'FetchURL,' + url
        self.__timeout = 20
        
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
                # if resp.status != 200: continue
                url = resp.headers.get('location')
                logger.info('real url is %s', resp.headers.get('location'))
                from .wsecrawlerfactory import factory
                factory.put_task(Output(url))
        except Exception as err:
            logger.error('Worker-%d, request to url(%s) fail, %s', id, self.__url, err)

class Output(Task):
    file = open(get_root_path()+'/output/result.txt', 'w+')

    def __init__(self, url):
        self.__url = url
        self.__name = 'Output'

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

class Parser(Task):
    def __init__(self, html):
        self.__html = html
        self.__name = 'Parser'

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
        logger.debug('Parser entry')
        from bs4 import BeautifulSoup as bs
        soup = bs(self.__html, 'lxml')
        links = soup.find_all('a')
        for link in links:
            if link.get('data-click') is None or link.get('data-click') == '': continue
            target_url = link.get('href')
            if target_url is not None and 'link?url=' in target_url:
                from .wsecrawlerfactory import factory
                factory.put_task(FetchURL(target_url))