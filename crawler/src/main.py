#!/usr/bin/env python
#coding=utf-8

import gevent
import time
from Crawler import crawler
from Crawler.Tasks.tasks import *

if __name__ == '__main__':

    request = HTMLRequest('http://www.zs.e21.edu.cn/ ')#('http://www.qdcdc.org:7004/main') #('http://127.0.0.1:8000/')
    crawler.crawler_singleton.put_task(request)
    #try:
    #    r=HTMLRequest.http.request('GET', 'http://127.0.0.1:8000/', timeout=10)
    #except Exception as err:
    #    print(err)

    while True:
        time.sleep(3)