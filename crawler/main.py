#!/usr/bin/env python
#coding=utf-8

import gevent
import time
from TaskManager import MyExampleTask, Task, TaskFactory

import urllib3
class HTMLRquest(Task):
    def __init__(self, url):
        self.__url = url
        self.__http=urllib3.PoolManager()
    
    @property
    def job(self):
        return self.__request_job
    
    def __request_job(self)
        try:
            self.__http.request('GET', self.__url)
        except Exception as err:
            print('Request to url(%s) fail, %s' % (self.__url, err))
        
class PageHandler():
    def __init__(self, url):
        self.url = url
        
class Crawler(object):
    def __init__(self, start=True, url):
        print('crawler')
        
        if start:
            self.start(url)
        
    def start(self, url):
        self.f = TaskFactory()







def task_producer(i, factory):
    while True:
        factory.put_task(MyExampleTask('task_producer', 0))
        time.sleep(0.5)
    

if __name__ == '__main__':
    
    gevent.joinall([gevent.spawn(task_producer, i, f) for i in range(10)])