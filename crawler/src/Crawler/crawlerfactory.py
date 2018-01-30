import gevent
import gevent.monkey
gevent.monkey.patch_all()
import time

from Crawler.Tasks.base import TaskFactory
from Crawler.Util.tools import logger

class CrawlerFactory(TaskFactory):
    def __init__(self):
        super().__init__()

    # Dispatch tasks
    def manager(self):
        self.__dispatcher()

    def start_crawler(self, url):
        self.put_message(url)
        
        while True:
            time.sleep(3)
    
    # Dispatch the tasks when HTTP request.
    def __dispatcher(self):
        # Save all requested URLs to avoid requesting it twice.
        requested_urls = {}

        while True:
            url = self.wait_for_message()
            logger.debug('received message %s', url)

            if requested_urls.get(url) is not None:
                logger.info('URL %s was requested in the past, skipped it.', url)
                continue

            requested_urls.update({url:True})

            logger.debug('URL is ok, %s', url)

            from .Tasks.tasks import HTMLRequest
            r = HTMLRequest(url)
            self.put_task(r)

factory = CrawlerFactory()
