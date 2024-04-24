from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
import string


def crawlerThread (frontier):
    while frontier:
        try:
            url = frontier.pop(0)
            url=url.replace('~', '')
            if 'https://www.cpp.edu' not in url and '@' not in url:
                url = 'https://www.cpp.edu'+url  
            print('opening url:', url, end='\n')                
            html = urlopen(url)
            #bs = BeautifulSoup(html.read(), 'html.parser')
            #if bs.find(re.compile('h[1-6]'), text = re.compile('Permanent Faculty')):
            if url == 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml':
                frontier.clear()
                bs = BeautifulSoup(html.read(), 'html.parser')
                names = bs.findAll('h2', id = None)
                infos = bs.findAll('p', class_ = None)
                for name, info in zip(names, infos):
                    #print(name.getText().strip(), end='\n')
                    #print(info.getText())
                    data = info.getText().replace('Email:  ', 'Email: ').replace('Web:  ', 'Web: ')
                    #print(data)
                    data = data.split('  ')
                    #print(data)

                    #print(data[0].replace('\xa0', '').replace('Title: ', '').replace(' Title:', '').replace('Title:', ''), end='\n')
                    #print(data[1].replace('\xa0', '').replace('Office:', '').replace(' ', ''), end='\n')
                    #print(data[2].replace('\xa0', '').replace('Phone:', '').replace(' ', ''), end='\n')
                    #print(data[3].replace('\xa0', '').replace('Email:', '').replace(' ', ''), end='\n')
                    #print(data[4].replace('\xa0', '').replace('Web:', '').replace(' ', ''), end='\n')
                    #print() 

                    db.faculty.insert_one({'name':name.getText().strip(), 
                                           'title':data[0].replace('\xa0', '').replace('Title: ', '').replace(' Title:', '').replace('Title:', ''), 
                                           'office':data[1].replace('\xa0', '').replace('Office:', '').replace(' ', ''), 
                                           'phone':data[2].replace('\xa0', '').replace('Phone:', '').replace(' ', ''), 
                                           'email':data[3].replace('\xa0', '').replace('Email:', '').replace(' ', ''), 
                                           'website':data[4].replace('\xa0', '').replace('Web:', '').replace(' ', '')})
            else:
                bs = BeautifulSoup(html.read(), 'html.parser')
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
db.faculty.drop()
crawlerThread(frontier)