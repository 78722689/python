#!/usr/bin/env python
#coding=utf-8

if __name__ == '__main__':
    from src.tools import logger
    from src.wsecrawlerfactory import factory
    
    
    factory.start_crawler(['asp?id='], 2, 100)