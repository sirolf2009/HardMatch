__author__= 'BHussain'
from py2neo import neo4j,node,rel

import requests
from bs4 import BeautifulSoup

def mediaMarkt_spider():
    url = 'http://www.mediamarkt.nl/mcs/productlist/Videokaarten,10259,482720.html?langId=-11'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    substring1 = 'Videokaart'
    substring2 = 'Grafische Kaart'
    for tekst in soup.findAll('a'):
        title = tekst.string
        if title is not None:
            if substring1 in title:
                href = 'http://www.mediamarkt.nl' + tekst.get('href')
                videoKaartFactory(href)
            elif substring2 in title:
                href = 'http://www.mediamarkt.nl' + tekst.get('href')
                videoKaartFactory(href)

def expr(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    substring1 = 'Controller'
    for td in soup.findAll('td',{'class':'kopsf'}):
        content = td.find('a').contents[0]
        #print(content)
        if substring1 in content:
            link ='http://www.informatique.nl'+(td.find('a')['href'])
            print(link)

def getNextPage(link):
    source_code = requests.get(link)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    currentPage = soup.find('a',{'id':'active'})
    currentPageNumber = int(currentPage.string)
    nextPage = currentPageNumber+1
    substring = 'p='+str(nextPage)
    for url in soup.findAll('a'):
        adress = url.get('href')
        if adress is not None:
            if substring in adress:
                url = 'http://www.informatique.nl/'+adress
                print(url)
                return(url)


getNextPage('http://www.informatique.nl/?m=USL&&sort=pop&g=699&view=&p=2')