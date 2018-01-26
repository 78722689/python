from bs4 import BeautifulSoup as bs
from Crawler.Util.tools import *
from Crawler import crawler
from urllib.parse import urlparse

class Parser():
    def __init__(self, id, page, host, url):
        self.__id = id
        self.__soup = bs(page, 'lxml')
        self.__host = host
        self.__current_url = url

    def __is_target_host(self, url):
        '''
        To check whether the URL corresponding host is the target host.
        :param url:
        :return: False;True
        '''
        host_ip = get_host_ip(url)
        logger.debug('Worker-%d, checking host(%s) VS host(%s)', self.__id, self.__host,host_ip)
        if host_ip == '': return False
        
        return [False, True][self.__host == host_ip]

    def __is_a_module_of_current_url(self, url):
        '''
        To check whether the url in this page is the subdomain of current URL
        eg. 'qq.com' in 'vip.qq.com', it means vip.qq is a module of qq.com
        '''

        if url == self.__current_url:return False
        
        return [False, True][get_hostname(self.__current_url).replace('www', '') in  get_hostname(url).replace('www', '')]
    
    def __is_a_sub_url(self, url):
        p = urlparse(url)
        if p.scheme != '' and p.hostname != '' and p.path == '':
            return False
        
        feature = ['/', '&', '=', '?']
        for f in feature:
            if f in url:
                return True

        return False
            
    def __is_contain_injection_character(self, url):
        '''
        To check whether the url contains '='
        '''
    
        injection_characters = ['=']
        for c in injection_characters:
            if c in url:
                return True
        
        return False
    
    def parse(self):
        links = self.__soup.find_all('a')
        logger.debug('Worker-%d, found %d URLs in page %s', self.__id, len(links), self.__current_url)

        index = 0
        # Find out all URLs from looping tags of 'a'
        for link in links:
            url = link.get('href')
            logger.debug('Worker-%d, found %d url %s in page, checking...', self.__id, ++index, url)

            need_continue = False
            # Check whether the host of this link is the target host
            if self.__is_a_module_of_current_url(url):
                logger.debug('Worker-%d, found module url %s in page', self.__id, url)
                need_continue = True
            elif self.__is_a_sub_url(url):
                logger.debug('Worker-%d, found sub url %s in page', self.__id, url)
                need_continue = True
                #url = get_hostname(self.__current_url) + url
                p = urlparse(self.__current_url)
                
                temp_url = p.scheme+':\\' if p.scheme != '' else '' 
                temp_url = temp_url+p.hostname+':'+p.port if p.port != '' else temp_url+p.hostname
                temp_url = temp_url+url if url[0] = '/' else '/' + url
                
                url = temp_url
                
            elif self.__is_target_host(url):
                logger.debug('Worker-%d, found target url %s in page', self.__id, url)
                need_continue = True
                
            if need_continue:
                logger.debug('Worker-%d, Put message to dispatch for url %s.....', self.__id, url)
                crawler.crawler_singleton.put_message(url)
                
                if self.__is_contain_injection_character(url):
                    from .tasks import Injection
                    injection = Injection(url)
                    crawler.crawler_singleton.put_task(injection)
            else:
                logger.debug('Worker-%d, No need to do more for url %s', url)