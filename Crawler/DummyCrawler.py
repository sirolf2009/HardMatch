__author__ = 'Basit'
import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, Node, Relationship, Graph
from pymongo import MongoClient
import IParseSave

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

def getCategories():
    c1 = Category('Moederbord', ['Intel', 'AMD'])
    c2 = Category('Processor', ['Intel Desktop', 'AMD Desktop'])
    c3 = Category('Video', ['NVIDIA','AMD'])
    c4 = Category('Geheugenmodules', ['DDR4','DDR3','DDR2'])
    c5 = Category('Harddisks', ['SATA','inch', 'Solid State Drive'])
    categories = [c1, c2, c3, c4, c5]
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
    elif subcat in 'Intel' or subcat in 'AMD':
        type = 'Motherboard'
    elif subcat in 'Intel Desktop' or subcat in 'AMD Desktop':
        type = 'Processor'
    elif subcat in 'NVIDIA' or subcat in 'AMD':
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
    elif 'SATA' in subcat or 'Solid State Drive' in subcat or 'inch' in subcat:
        type = 'Storage'
    elif 'intern' in subcat or 'extern' in subcat:
        type = 'Optical drive'
    return type

def getHTML(url):
    # print(url)
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
        link = section.get('href') + '?spcall=yes'
        if label == 'Motherboard':
            Motherboard.motherBoardParser(link)
        elif label == 'Processor':
            CPU.cpuParser(link)
        elif label == 'Graphics card':
            GraphicsCard.graphicsCardParser(link)
        elif label == 'RAM':
            RAM.RAMparser(link)
        elif label == 'Storage':
            Storage.storageParser(link)
    if getNextPage(url) is not None:
        lowLevelSpider(getNextPage(url), label)

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

class CPU(IParseSave.CPU):

    def cpuParser(detailadress):
        cpu = CPU()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})
        product = soup.find('h1')
        product = product.string
        splitStrings = product.split(',')
        cpu.properties['product'] = splitStrings[0]
        brand = soup.find('span', {'itemprop': 'brand'})
        cpu.properties['brand'] = brand.string
        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace(',', '.')
        cpu.properties['price'] = float(price[2:])

        for x in specs:
            if 'Type' in x.string:
                cpu.properties['serie'] = x.findNextSibling('td').string
            elif 'socket' in x.string:
                cpu.properties['socket'] = x.findNextSibling('td').string
            elif 'cores' in x.string:
                cpu.properties['amountOfCores'] = x.findNextSibling('td').string
            elif 'snelheid' in x.string:
                cpu.properties['speed'] = x.findNextSibling('td').string
            elif 'TDP' in x.string:
                cpu.properties['thermalDesignPower'] = x.findNextSibling('td').string
            elif 'Graphics' in x.string:
                cpu.properties['intergratedGraphics'] = x.findNextSibling('td').string
            elif 'L1' in x.string:
                cpu.properties['CPUCacheLevel1'] = x.findNextSibling('td').string
            elif 'L2' in x.string:
                cpu.properties['CPUCacheLevel2'] = x.findNextSibling('td').string
            elif 'L3' in x.string:
                cpu.properties['CPUCacheLevel3'] = x.findNextSibling('td').string

        IParseSave.saveComponent(cpu.properties,winkel)

class GraphicsCard(IParseSave.GraphicsCard):

    def graphicsCardParser(detailadress):
        gc = GraphicsCard()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})


        product = soup.find('h1')
        product = product.string
        splitStrings = product.split(',')
        gc.properties['product'] = splitStrings[0]

        brand = soup.find('span', {'itemprop': 'brand'})
        gc.properties['brand'] = brand.string

        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace(',', '.')
        gc.properties['price'] = float(price[2:])

        for x in specs:
            if 'Fabrikant' in x.string:
                gc.properties['videochipManufacturer'] = x.findNextSibling('td').string
            elif 'GPU kloksnelheid' in x.string:
                gc.properties['nominalSpeedVideochip'] = x.findNextSibling('td').string
            elif 'kernen' in x.string:
                gc.properties['calculatingCores'] = x.findNextSibling('td').string
            elif 'hoeveelheid' in x.string:
                gc.properties['memoryCapacity'] = x.findNextSibling('td').string
            elif 'geheugentype' in x.string:
                gc.properties['memoryType'] = x.findNextSibling('td').string
            elif 'Geheugen kloksnelheid' in x.string:
                gc.properties['memorySpeed'] = x.findNextSibling('td').string
            elif 'bandbreedte'in x.string:
                gc.properties['memoryBusWidth'] = x.findNextSibling('td').string
            elif 'Bus type' in x.string:
                gc.properties['cardInterface'] = x.findNextSibling('td').string
            elif 'DirectX' in x.string:
                gc.properties['directXversion'] = x.findNextSibling('td').string
            elif 'OpenGL' in x.string:
                gc.properties['openGLversion'] = x.findNextSibling('td').string
            elif 'sloten' in x.string:
                gc.properties['amountOfSlots'] = x.findNextSibling('td').string

        IParseSave.saveComponent(gc.properties,winkel)

class Motherboard(IParseSave.Motherboard):
    def motherBoardParser(detailadress):
        mb = Motherboard()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})

        product = soup.find('h1')
        product = product.string
        splitStrings = product.split(',')
        mb.properties['product'] = splitStrings[0]

        brand = soup.find('span', {'itemprop': 'brand'})
        mb.properties['brand'] = brand.string

        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace(',', '.')
        mb.properties['price'] = float(price[2:])

        socket = soup.find('span', {'itemprop':'description'})
        socket = socket.text
        splitStrings = socket.split()
        socket = splitStrings[2]
        socket_final = socket
        mb.properties['socket'] = socket_final

        serie = soup.find('span',{'itemprop':'title'})
        serie = serie.string
        mb.properties['serie'] = serie

        for x in specs:
            if 'geheugensloten' in x.string:
                mb.properties['amountOfSockets'] = x.findNextSibling('td').string
            elif 'Form factor' in x.string:
                mb.properties['formFactor'] = x.findNextSibling('td').string
            elif 'Chipset' in x.string:
                mb.properties['motherboardChipset'] = x.findNextSibling('td').string
            elif 'Type geheugen' in x.string:
                mb.properties['memoryType'] = x.findNextSibling('td').string
            elif 'PCI-E x16 sloten' in x.string:
                mb.properties['amountOfPCIex16slots'] = x.findNextSibling('td').string

        IParseSave.saveComponent(mb.properties,winkel)

class RAM(IParseSave.RAM):
    def RAMparser(detailadress):
        ram = RAM()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})

        product = soup.find('h1')
        product = product.string
        splitStrings = product.split(',')
        ram.properties['product'] = splitStrings[0]

        brand = soup.find('span', {'itemprop': 'brand'})
        ram.properties['brand'] = brand.string

        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace(',', '.')
        ram.properties['price'] = float(price[2:])

        type = soup.find('span', {'itemprop':'description'})
        type = type.text
        splitStrings = type.split()
        type = splitStrings[2]
        type_final = type
        ram.properties['memoryType'] = type_final

        for x in specs:
            if 'capactiteit' in x.string:
                ram.properties['memoryCapacity'] = x.findNextSibling('td').string
            elif 'modules' in x.string:
                ram.properties['amount'] = x.findNextSibling('td').string
            elif 'Latency' in x.string:
                ram.properties['memoryCASLatency'] = x.findNextSibling('td').string
            elif 'Voltage' in x.string:
                ram.properties['voltage'] = x.findNextSibling('td').string

        IParseSave.saveComponent(ram.properties,winkel)

class Storage(IParseSave.Storage):
    def storageParser(detailadress):
        store = Storage()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})

        product = soup.find('h1')
        product = product.string
        store.properties['product'] = product

        brand = soup.find('span', {'itemprop': 'brand'})
        store.properties['brand'] = brand.string

        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace(',', '.')
        store.properties['price'] = float(price[2:])

        for x in specs:
            if 'Capaciteit' in x.string:
                store.properties['memoryCapacity'] = x.findNextSibling('td').string
            if 'Dikte' in x.string:
                store.properties['height'] = x.findNextSibling('td').string
            if 'Rotatiesnelheid' in x.string:
                store.properties['rotationSpeed'] = x.findNextSibling('td').string
            if 'Chache' in x.string:
                store.properties['driveCache'] = x.findNextSibling('td').string

        IParseSave.saveComponent(store.properties,winkel)

graph = Graph("http://localhost:7474/db/data/")
winkel = Node('Store', Naam='informatique.nl')
graph.create(winkel)
topLevelSpider('http://www.informatique.nl/componenten/', getCategories())