#!/usr/bin/env python
#coding=utf-8

import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time
#from Crawler.crawler import factory

if __name__ == '__main__':
    #factory.put_message('http://www.zs.e21.edu.cn/')#('http://www.bhxww.com/')#('http://www.qdcdc.org:7004/main')
    import os
    import sys
    print(os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)))
    #while True:
    #    time.sleep(3)