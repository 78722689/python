from Crawler.Tasks.base import TaskFactory
from Crawler.Util.tools import logger

class CrawlerFactory(TaskFactory):
    def __init__(self):
        super().__init__()

    def manager(self):
        # Save all requested URLs
        requested_urls = {}

        while True:
            msg = self.wait_for_message()
            logger.debug('received message %s', msg)

            if requested_urls.get(msg) is not None:
                logger.info('URL %s was requested in the past, skip it.', msg)
                continue

            requested_urls.update({msg:True})

            logger.debug('URL is ok, %s', msg)

            from .Tasks.tasks import HTMLRequest
            r = HTMLRequest(msg)
            self.put_task(r)

    def start_crawler(self, url):
        print('start')

crawler_singleton = CrawlerFactory()
