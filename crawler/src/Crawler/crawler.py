from Crawler.Tasks.base import TaskFactory

class CrawlerFactory(TaskFactory):
    def __init__(self):
        super().__init__()

    def manager(self):
        print('manager')

    def start_crawler(self, url):
        print('start')

crawler_singleton = CrawlerFactory()
