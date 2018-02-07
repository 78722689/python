import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time

from .base import TaskFactory
from .tasks import Baidu

BAIDU = 1
BING = 2
SO = 3

class WSECrawlerFactory(TaskFactory):
    def __init__(self):
        super().__init__(start=False)

    def start_crawler(self, keywords, page_num, coroutine_num, engine=BAIDU):
        self.start(coroutine_num, coroutine_num)
        
        for keyword in keywords:
            for pn in range(page_num):
                self.put_task(Baidu(keyword, pn))
        
        while True:
            time.sleep(3)

factory = WSECrawlerFactory()
