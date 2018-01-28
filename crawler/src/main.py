#!/usr/bin/env python
#coding=utf-8

import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time
from Crawler import crawler
from Crawler.Tasks.tasks import *

def task_producer(id):
    logger.debug('task-%d started', id)

    request = HTMLRequest('http://www.bhxww.com/')#('http://www.zs.e21.edu.cn/ ')  # ('http://www.qdcdc.org:7004/main') #('http://127.0.0.1:8000/')
    crawler.crawler_singleton.put_task(request)


if __name__ == '__main__':
    #gevent.joinall([gevent.spawn(task_producer, i) for i in range(1000)])
    #request = HTMLRequest('http://www.qdcdc.org:7004/main') #('http://www.zs.e21.edu.cn/ ')##('http://127.0.0.1:8000/')
    #crawler.crawler_singleton.put_task(request)
    crawler.crawler_singleton.put_message('http://www.bhxww.com/')#('http://www.qdcdc.org:7004/main')

    #try:
    #    r=HTMLRequest.http.request('GET', 'http://127.0.0.1:8000/', timeout=10)
    #except Exception as err:
    #    print(err)

    while True:
        time.sleep(3)