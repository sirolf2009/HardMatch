__author__ = 'Basit'
import requests
from bs4 import BeautifulSoup
from py2neo import neo4j,Node, Relationship,Graph


def getCategories():
    c1 = Category('Controller', ['Controllers'])
    c2 = Category('Behuizingen', ['PC Behuizing', 'Voeding', 'Ventilatoren'])
    c3 = Category('Moederbord', ['Intel', 'AMD', 'CPU'])
    c4 = Category('Processor', ['Intel Desktop', 'AMD Desktop'])
    c5 = Category('Video', ['kaarten'])
    c6 = Category('Geluid', ['Geluidskaart (intern)', 'Geluidskaarten (extern)'])
    c7 = Category('Koeling', ['Grills','Grafische kaart Koelers', 'Waterkoeling', 'Fancontrollers','Processor Koelers'])
    c8 = Category('Geheugenmodules', ['DDR'])
    c9 = Category('Harddisks', ['Harddisks', 'Solid State Drive'])
    c10 = Category('CD', ['intern', 'extern'])
    categories = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
    return categories


def topLevelSpider(url, categories):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for td in soup.findAll('td', {'class': 'kopsf'}):
        content = td.find('a').contents[0]
        for i in range(len(categories)):
            if categories[i].getName() in content:
                link = 'http://www.informatique.nl' + (td.find('a')['href'])
                midLevelSpider(link, categories[i].getSubs())


def midLevelSpider(url, subs):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for td in soup.findAll('td', {'class': 'kopsf'}):
        content = td.find('a').contents[0]
        for i in range(len(subs)):
            if subs[i] in content:
                link = 'http://www.informatique.nl' + (td.find('a')['href'])
                lowLevelSpider(link)


def lowLevelSpider(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for section in soup.findAll('a', {'class': 'product_overlay'}):
        # print(section.get('href'))
        componentFactory(section.get('href'))
    if getNextPage(url) is not None:
        lowLevelSpider(getNextPage(url))


def componentFactory(detailadress):
    source_code = requests.get(detailadress)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    naam_raw = soup.find('h1')
    naam_clean = naam_raw.string
    prijs_raw = soup.find('p', {'class': 'verkoopprijs'})
    prijs_clean = prijs_raw.string
    c = Component()
    Component.addGegeven(c, 'Naam', naam_clean)
    Component.addGegeven(c, 'Prijs', prijs_clean)
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
    #Component.printGegevens(c)
    Component.saveComponent(c)


def getNextPage(link):
    source_code = requests.get(link)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
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

    def saveComponent(self):
        cn = Node(naam= self.gegevens['Naam'])
        winkel.pull()
        for i in self.gegevens:
            cn.properties[i]=self.gegevens[i]
        graph = Graph("http://localhost:7474/db/data/")
        rel = Relationship(cn,'Verkocht bij',winkel,prijs=self.gegevens['Prijs'])
        graph.create(cn)
        graph.create(rel)





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

# lowLevelSpider('http://www.informatique.nl/?M=USL&G=004')
#componentFactory('http://www.informatique.nl/445263/conceptronic-csata600exi-2xsata-2xesata.html')
'''categories = getCategories()
for i in range(len(categories)):
    Category.printCategory(categories[i])'''
#lowLevelSpider('http://www.informatique.nl/?M=USL&G=004')
'''graph = Graph("http://localhost:7474/db/data/")
cn = Node('testing',message = 'Hello World')
graph.create(cn)'''
graph = Graph("http://localhost:7474/db/data/")
winkel = Node(type='Winkel', Naam='informatique.nl')
graph.create(winkel)
#componentFactory('http://www.informatique.nl/543088/msi-x99s-sli-plus.html')
topLevelSpider('http://www.informatique.nl/componenten/', getCategories())
#lowLevelSpider('http://www.informatique.nl/?M=ART&G=024')



