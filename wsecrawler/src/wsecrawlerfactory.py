import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time
import urllib
from .base import TaskFactory
from .tasks import Baidu, FetchURL
from .tools import logger

BAIDU = 1
BING = 2
SO = 3

class WSECrawlerFactory(TaskFactory):
    def __init__(self):
        self.__request_status = {}
        self.__exit = False
        super().__init__(start=False)

    def manager(self):
        count = 0

        while not self.__exit:
            msg = self.wait_for_message()
            logger.debug('Received page status %d count %d', msg['page'], msg['count'])
            if msg['count'] > 0:
                self.__request_status[msg['page']] = msg['count']
                continue
            elif msg['count'] == 0:
                self.__request_status[msg['page']] = 0
            else:
                self.__request_status[msg['page']] = self.__request_status[msg['page']] + msg['count']

            if self.__request_status[msg['page']] == 0:
                count += 1
                logger.info('Page %d finished the URLs request.', msg['page'] )
            if len(self.__request_status) == count: self.__exit = True
            logger.debug('Page(%d)  len(__request_status)(%d) VS count(%d)', msg['page'], len(self.__request_status), count)
        logger.info('Manager exit!')

    def start_crawler(self, keywords, page_num, coroutine_num, engine=BAIDU):
        for pn in range(page_num):
            self.__request_status[pn] = 0
        self.start(1024, coroutine_num)

        for keyword in keywords:
            keyword = urllib.parse.quote(keyword)
            for pn in range(page_num):
                engine = Baidu(keyword, pn)
                engine.request(pn)
        
        while not self.__exit:
            time.sleep(3)

        logger.info('Main exit!')

factory = WSECrawlerFactory()
