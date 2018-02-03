#!/usr/bin/env python
#coding=utf-8
import argparse

def initparser():
    """initialize parser arguments"""

    global parser
    parser = argparse.ArgumentParser(description='A crawler tool for finding out what you want from a website.')
    parser.add_argument("-t", dest="target", help="scan target website", type=str, metavar="www.example.com")
    parser.add_argument('-r', dest="routines", help="concurrent routines number", type=int, default=1024)
    parser.add_argument('-o', dest="output", help="the log output file", type=str, default='.')
    parser.add_argument('-m', dest="maxsize", help="the max socket size per host allowed to open", type=int, default=128)
    parser.add_argument('-l', dest="loglevel", help="the log level", type=int, default=1)

# Testing data
# #('http://www.bhxww.com/')#('http://www.qdcdc.org:7004/main') ('http://www.zs.e21.edu.cn/')
if __name__ == '__main__':
    initparser()
    args = parser.parse_args()

    log_file = ''
    if args.output:
        log_file = args.output

    #log_level = 1
    #if args.silent:
    #    log_level = 4

    from Crawler.Util.tools import logger
    logger.set(log_file, args.loglevel)

    if args.target is None or args.target == '':
        logger.error('Crawl URL is empty, please specify a valid and try again.')

    from Crawler.crawlerfactory import factory
    factory.start_crawler(args.target, args.routines)