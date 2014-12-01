__author__ = 'Basit'
import time

import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, Node, Relationship, Graph
from pymongo import MongoClient


def getCategories():
    c1 = Category('Controller', ['Controllers'])
    c2 = Category('Behuizingen', ['PC Behuizing', 'Voeding', 'Ventilatoren'])
    c3 = Category('Moederbord', ['Intel', 'AMD', 'CPU'])
    c4 = Category('Processor', ['Intel Desktop', 'AMD Desktop'])
    c5 = Category('Video', ['Videokaarten'])
    c6 = Category('Geluid', ['Geluidskaart (intern)', 'Geluidskaarten (extern)'])
    c7 = Category('Koeling',
                  ['Grills', 'Grafische kaart Koelers', 'Waterkoeling', 'Fancontrollers', 'Processor Koelers'])
    c8 = Category('Geheugenmodules', ['DDR'])
    c9 = Category('Harddisks', ['Harddisks', 'Solid State Drive'])
    c10 = Category('CD', ['intern', 'extern'])
    categories = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
    return categories


def determineProductType(subcat):
    if subcat in 'Controllers':
        type = 'Controller'
    elif subcat in 'PC Behuizing':
        type = 'Case'
    elif subcat in 'Voeding':
        type = 'Power Supply'
    elif subcat in 'Ventilatoren':
        type = 'Fans'
    elif subcat in 'Intel' or subcat in 'AMD' or subcat in 'CPU':
        type = 'Motherboard'
    elif subcat in 'Intel Desktop' or subcat in 'AMD Desktop':
        type = 'Processor'
    elif subcat in 'Videokaarten':
        type = 'Graphics card'
    elif 'Geluidskaart' in subcat:
        type = 'Sound card'
    elif 'Grills' in subcat:
        type = 'Fan guard'
    elif 'Grafische kaart Koelers' in subcat:
        type = 'Graphic card cooler'
    elif 'Waterkoeling' in subcat:
        type = 'Water cooling'
    elif 'Fancontrollers' in subcat:
        type = 'Fan controller'
    elif 'Processor Koelers' in subcat:
        type = 'Processor cooler'
    elif 'DDR' in subcat:
        type = 'RAM'
    elif 'Harddisks' in subcat or 'Solid State Drive' in subcat:
        type = 'HDD'
    elif 'intern' in subcat or 'extern' in subcat:
        type = 'Optical drive'
    return type


def getHTML(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup


def topLevelSpider(url, categories):
    soup = getHTML(url)
    for td in soup.findAll('td', {'class': 'kopsf'}):
        content = td.find('a').contents[0]
        for i in range(len(categories)):
            if categories[i].getName() in content:
                link = 'http://www.informatique.nl' + (td.find('a')['href'])
                midLevelSpider(link, categories[i].getSubs())


'''def navSpider(url, categories):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for td in soup.findAll('td', {'class': 'kopsf'}):
        content = td.find('a').contents[0]
        for i in range(len(categories)):
            if categories[i].getName() in content:
                link = 'http://www.informatique.nl' + (td.find('a')['href'])
                print(categories[i].getName())
                navSpider(link, categories)
            else:
                subs = categories[i].getSubs()
                for i in range(len(subs)):
                    if subs[i] in content:
                        #link = 'http://www.informatique.nl' + (td.find('a')['href'])
                        label = determineProductType(subs[i])
                        print(subs[i])
                        #lowLevelSpider(link,label)'''


def midLevelSpider(url, subs):
    soup = getHTML(url)
    for td in soup.findAll('td', {'class': 'kopsf'}):
        content = td.find('a').contents[0]
        for i in range(len(subs)):
            if subs[i] in content:
                link = 'http://www.informatique.nl' + (td.find('a')['href'])
                label = determineProductType(subs[i])
                lowLevelSpider(link, label)


def lowLevelSpider(url, label):
    soup = getHTML(url)
    for section in soup.findAll('a', {'class': 'product_overlay'}):
        # print(section.get('href'))
        componentFactory(section.get('href'), label)
    if getNextPage(url) is not None:
        lowLevelSpider(getNextPage(url), label)


def componentFactory(detailadress, label):
    soup = getHTML(detailadress)
    naam_raw = soup.find('h1')
    naam_clean = naam_raw.string
    prijs_raw = soup.find('p', {'class': 'verkoopprijs'})
    prijs_clean = prijs_raw.string
    prijs_tussen = prijs_clean.replace(',', '.')
    prijs_final = float(prijs_tussen[2:])
    merk_raw = soup.find('span', {'itemprop': 'brand'})
    merk_clean = merk_raw.string
    c = Component()
    Component.addGegeven(c, 'Naam', naam_clean)
    Component.addGegeven(c, 'Prijs', prijs_final)
    Component.addGegeven(c, 'Merk', merk_clean)
    voorraadChecker(detailadress,c)
    algemeen = soup.find('table', {'id': 'details'})
    specs = soup.find('table', {'class': 'specs left'})
    if algemeen is not None:
        for omschrijving in algemeen.findAll('td', {'class': 'right'}):
            key = omschrijving.string
            if key is not None:
                raw_value = omschrijving.findNextSibling('td')
                value = raw_value.string
                Component.addGegeven(c, key, value)
    if specs is not None:
        for omschrijving in specs.findAll('td', {'class': 'right'}):
            key = omschrijving.string
            if key is not None:
                raw_value = omschrijving.findNextSibling('td')
                value = raw_value.string
                Component.addGegeven(c, key, value)
    Component.saveMetaData(c)
    Component.saveComponent(c, label)

def voorraadChecker(url,c):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    substring = 'Online op voorraad'
    for x in soup.find('td', {'style':'padding:5px 4px 5px 4px;line-height:2'}):
        if x is not None:
                if substring in x.text:
                    voorraad = 1
                    Component.addGegeven(c,'voorraadstatus',voorraad)


def getNextPage(link):
    soup = getHTML(link)
    currentPage = soup.find('a', {'id': 'active'})
    if currentPage is not None:
        currentPageNumber = int(currentPage.string)
        nextPage = currentPageNumber + 1
        substring = 'p=' + str(nextPage)
        for url in soup.findAll('a'):
            adress = url.get('href')
            if adress is not None:
                if substring in adress:
                    url = 'http://www.informatique.nl/' + adress
                    return url
    return None


class Component():
    gegevens = {}

    def addGegeven(self, key, value):
        self.gegevens[key] = value

    def printGegevens(self):
        for x in self.gegevens:
            print(x)
            print(self.gegevens[x])

    def saveComponent(self, label):
        cn = Node(label)
        winkel.pull()
        for i in self.gegevens:
            cn.properties[i] = self.gegevens[i]
        graph = Graph("http://localhost:7474/db/data/")
        rel = Relationship(cn, 'Sold at', winkel, prijs=self.gegevens['Prijs'])
        graph.create(cn)
        graph.create(rel)

    def saveMetaData(self):
        client = MongoClient()
        db = client.productdatabase
        collection = db.informatiquemeta
        millis = int(round(time.time() * 1000))
        metadata = {
            'Naam': self.gegevens['Naam'],
            'Prijs': self.gegevens['Prijs'],
            'Website': 'Informatique.nl',
            'Tijd&Datum': millis
        }
        collection.insert(metadata)


class Category():
    name = ''
    subs = []

    def __init__(self, name, subs):
        self.name = name
        self.subs = list(subs)

    def setName(self, name):
        self.name = name

    def setSubs(self, subs):
        self.subs = list(subs)

    def getName(self):
        return self.name

    def getSubs(self):
        return self.subs

    def printCategory(self):
        print(self.name)
        for i in range(len(self.subs)):
            print(self.subs[i])


graph = Graph("http://localhost:7474/db/data/")
winkel = Node('Store', Naam='informatique.nl')
graph.create(winkel)
topLevelSpider('http://www.informatique.nl/componenten/', getCategories())

