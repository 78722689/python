from bs4 import BeautifulSoup as bs



class Parser():
    def __init__(self, page):
        self.__soup = bs(page, 'lxml')
    def __remove_url():
    
    def parse(self):
        print(self.__soup.title)
        #with open('/mnt/python/output/page.html', 'w+') as f: #open('E:\Programing\python\python\crawler\output\page.html', 'w') as f:
        #    f.write(str(self.__soup.prettify()))
        #    f.flush()
        #print(self.__soup.prettify())
        
        # Find out all URLs from looping tags of 'a'
        for link in self.__soup.find_all('a'):
            print(link.get('href'))

