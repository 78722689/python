from bs4 import BeautifulSoup as bs
from Crawler.Util.tools import *


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

        return [False, True][self.__host == get_host_ip(url)]

    def __is_a_module_of_current_url(self, url):
        # eg. 'qq.com' in 'vip.qq.com', it means vip.qq is a module of qq.com
        return [False, True][get_hostname(self.__current_url).replace('www', '') in  get_hostname(url).replace('www', '')]


    def parse(self):
        print(self.__soup.title)
        print('==host=%s' % self.__host)
        #with open('/mnt/python/output/page.html', 'w+') as f: #open('E:\Programing\python\python\crawler\output\page.html', 'w') as f:
        #    f.write(str(self.__soup.prettify()))
        #    f.flush()
        #print(self.__soup.prettify())

        module_domain_url = []
        # Find out all URLs from looping tags of 'a'
        for link in self.__soup.find_all('a'):
            url = link.get('href')
            print('Checking.....%s' % url)
            # Check whether the host of this link is the target host
            if self.__is_target_host(url):
                print('Found %s' % url)
            elif self.__is_a_module_of_current_url(url):
                print('Found module URL %s' % url)

