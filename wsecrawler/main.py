#!/usr/bin/env python
#coding=utf-8
import argparse
def initparser():
    """initialize parser arguments"""

    global parser
    parser = argparse.ArgumentParser(description='A crawler tool for searching the URLs from a Web Search Engine.')
    parser.add_argument("-e", dest="engine", help="The engine to do the search", type=str, metavar="baidu")
    parser.add_argument('-r', dest="routines", help="Concurrent routines number", type=int, default=1024)
    parser.add_argument('-o', dest="output", help="The log output file", type=str, default='.')
    parser.add_argument('-m', dest="maxsize", help="The max socket size per host allowed to open", type=int, default=128)
    parser.add_argument('-l', dest="loglevel", help="The log level", type=int, default=1)
    parser.add_argument('-t', dest="timeout", help="HTTP request timeout", type=int, default=20)
    parser.add_argument('-n', dest="number", help="The total page numbers to request", type=int, default=1)
    parser.add_argument('-i', dest="items", help="The item numbers per page", type=int, default=10)
    parser.add_argument('-k', dest="keywords", help="The keywords to search", type=str, default='')
    
if __name__ == '__main__':
    initparser()
    args = parser.parse_args()

    log_file = ''
    if args.output:
        log_file = args.output

    from src.tools import logger
    logger.set(log_file, args.loglevel)
    
    if len(args.keywords) == 0:
        logger.error('keywords is empty.')
        exit
    
    from src.wsecrawlerfactory import factory
    #factory.start_crawler(['inurl:asp?id=','inurl:product.php?id=', 'inurl:readnews.php?id='], 2, 100)
    factory.start_crawler(args.keywords.split(';'), args.number, args.number*10)
    #factory.start_crawler(['inurl:jsp?id='], 30, 100)