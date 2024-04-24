from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re


def crawlerThread (frontier):
    while frontier:
        try:
            url = frontier.pop(0)
            url=url.replace('~', '')
            if 'https://www.cpp.edu' not in url and '@' not in url:
                url = 'https://www.cpp.edu'+url  
            print('opening url:', url, end='\n')                
            html = urlopen(url)
            bs = BeautifulSoup(html.read(), 'html.parser')
            db.pages.insert_one({'url':url, 'html':html.read()})
            if bs.find(re.compile('h[1-6]'), text = re.compile('Permanent Faculty')):
            #if url == 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml':
                frontier.clear()
                print(bs.prettify())
            else:
                frontier.extend(a.get('href') for a in bs.findAll('a'))
                #for link in bs.findAll('a'):
                #    frontier.append(link.get('href'))
        except HTTPError as e:
            print(e)
        except URLError as e:
            print('server not found')

html = urlopen('https://www.cpp.edu/sci/computer-science/')
bs = BeautifulSoup(html.read(), 'html.parser')
frontier = [a['href'] for a in bs.findAll('a', {'href':re.compile('.html')})]
db = MongoClient(host = "localhost", port = 27017).documents
db.pages.drop()
crawlerThread(frontier)
