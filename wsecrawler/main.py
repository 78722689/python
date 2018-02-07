#!/usr/bin/env python
#coding=utf-8

if __name__ == '__main__':
    from src.wsecrawlerfactory import factory
    factory.start_crawler(['inurl:asp?id=','inurl:product.php?id=', 'inurl:readnews.php?id='], 2, 100)