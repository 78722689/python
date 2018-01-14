from bs4 import BeautifulSoup as bs

class Parser():
    def __init__(self, page):
        self.__soup = bs(page, 'lxml')

    def parse(self):
        print(self.__soup.title)
        with open('E:\Programing\python\python\crawler\output\page.html', 'w') as f:
            f.write(str(self.__soup.prettify()))
            f.flush()
        #print(self.__soup.prettify())

