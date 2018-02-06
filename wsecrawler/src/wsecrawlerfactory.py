import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time

from .base import TaskFactory
#from Crawler.Util.tools import logger

class WSECrawlerFactory(TaskFactory):
    def __init__(self):
        super().__init__(start=True)

    def start_crawler(self, keyword, page_num, coroutine_num):
        self.start(coroutine_num, coroutine_num)
        
        while True:
            time.sleep(3)

factory = WSECrawlerFactory()
