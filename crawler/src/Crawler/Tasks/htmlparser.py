from bs4 import BeautifulSoup as bs
from Crawler.Util.tools import *
from Crawler import crawler

class Parser():
    def __init__(self, page, host, url):
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
        print('__host(%s) == host_ip(%s)' % (self.__host,host_ip))
        
        return [False, True][self.__host == host_ip]

    def __is_a_module_of_current_url(self, url):
        '''
        To check whether the url in this page is the subdomain of current URL
        eg. 'qq.com' in 'vip.qq.com', it means vip.qq is a module of qq.com
        '''

        if url == self.__current_url:return False

        return [False, True][get_hostname(self.__current_url).replace('www', '') in  get_hostname(url).replace('www', '')]
    
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
        print(self.__soup.title)
        print('==host=%s' % self.__host)

        # Find out all URLs from looping tags of 'a'
        for link in self.__soup.find_all('a'):
            url = link.get('href')
            print('Checking.....%s' % url)
            
            need_continue = False
            # Check whether the host of this link is the target host
            if self.__is_a_module_of_current_url(url):
                print('Found %s' % url)
                need_continue = True
                if self.__is_contain_injection_character(url):
                    from .tasks import Injection
                    injection = Injection(url)
                    crawler.crawler_singleton.put_task(injection)

            elif self.__is_target_host(url):
                print('Found module URL %s' % url)
                need_continue = True
                if self.__is_contain_injection_character(url):
                    from .tasks import Injection
                    injection = Injection(url)
                    crawler.crawler_singleton.put_task(injection)

            if need_continue:
                print('HTTPRequest task send for url %s.....' % url)
                from .tasks import HTMLRequest
                r = HTMLRequest(url)
                crawler.crawler_singleton.put_task(r)
