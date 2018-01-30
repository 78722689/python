#!/usr/bin/env python
#coding=utf-8

from Crawler.crawlerfactory import factory
import argparse

def initparser():
    """initialize parser arguments"""

    global parser
    parser = argparse.ArgumentParser(description='A crawler tool for finding out what you want from a website.')
    parser.add_argument("-t", dest="target", help="scan target website", type=str, metavar="www.example.com")
    parser.add_argument('-r', dest="routines", help="concurrent routines number", type=int, default=1024)
    parser.add_argument('-o', dest="output", help="log output folder", type=str, default='.')
    parser.add_argument('-m', dest="maxsize", help="the max socket size per host allowed to open", type=int, default=128)

# Testing data
# #('http://www.bhxww.com/')#('http://www.qdcdc.org:7004/main') ('http://www.zs.e21.edu.cn/')
if __name__ == '__main__':
    initparser()
    args = parser.parse_args()
    if args.target is not None:
        factory.start_crawler(args.target)
