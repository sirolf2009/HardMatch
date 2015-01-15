#!/usr/bin/env python
# coding: utf8

# __author__ = 'Basit'
import requests
from bs4 import BeautifulSoup
from py2neo import Node, Graph

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
    c3 = Category('Video', ['NVIDIA', 'AMD'])
    c4 = Category('Geheugenmodules', ['DDR4', 'DDR3', 'DDR2'])
    c5 = Category('Harddisks', ['SATA', 'inch', 'Solid State Drive'])
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
        label = 'CPU'
        cpu = CPU()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})
        product = soup.find('h1')
        product = product.string
        splitStrings = product.split(',')
        cpu.properties['product'] = splitStrings[0]
        brand = soup.find('span', {'itemprop': 'brand'})
        cpu.properties['Merk'] = brand.string
        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace('.', '')
        price = price.replace(',', '.')
        price = float(price[2:])

        cpu.properties['Img'] = IParseSave.imgFinder(detailadress)

        if specs is not None:
            for x in specs:
                if x.string is not None:
                    if 'Fabrikantcode' in x.string:
                        cpu.properties['ModelID'] = x.findNextSibling('td').string
                    elif 'Type' in x.string:
                        cpu.properties['serie'] = x.findNextSibling('td').string
                    elif 'Socket' in x.string:
                        cpu.properties['Socket'] = x.findNextSibling('td').string
                    elif 'cores' in x.string:
                        cpu.properties['AantalCores'] = x.findNextSibling('td').string
                    elif 'snelheid' in x.string:
                        cpu.properties['Snelheid'] = x.findNextSibling('td').string
                    elif 'TDP' in x.string:
                        cpu.properties['ThermalDesignPower'] = x.findNextSibling('td').string
                    elif 'Graphics' in x.string:
                        cpu.properties['GeïntegreerdeGraphics'] = x.findNextSibling('td').string
                    elif 'L1' in x.string:
                        cpu.properties['CPUCacheLevel1'] = x.findNextSibling('td').string
                    elif 'L2' in x.string:
                        cpu.properties['CPUCacheLevel2'] = x.findNextSibling('td').string
                    elif 'L3' in x.string:
                        cpu.properties['CPUCacheLevel3'] = x.findNextSibling('td').string

        voorraad = IParseSave.voorraadChecker(detailadress)
        IParseSave.saveComponent(cpu.properties, label, price,voorraad,detailadress, winkel)


class GraphicsCard(IParseSave.GraphicsCard):
    def graphicsCardParser(detailadress):
        label = 'GraphicsCard'
        gc = GraphicsCard()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})

        product = soup.find('h1')
        product = product.string
        splitStrings = product.split(',')
        gc.properties['product'] = splitStrings[0]

        brand = soup.find('span', {'itemprop': 'brand'})
        gc.properties['Merk'] = brand.string

        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace('.', '')
        price = price.replace(',', '.')
        price = float(price[2:])

        gc.properties['Img'] = IParseSave.imgFinder(detailadress)

        if specs is not None:
            for x in specs:
                if x.string is not None:
                    if 'Fabrikantcode' in x.string:
                        gc.properties['ModelID'] = x.findNextSibling('td').string
                    elif 'Fabrikant' in x.string:
                        gc.properties['Videochipfabrikant'] = x.findNextSibling('td').string
                    elif 'GPU kloksnelheid' in x.string:
                        gc.properties['NominaleSnelheidVideochip'] = x.findNextSibling('td').string
                    elif 'kernen' in x.string:
                        gc.properties['Rekenkernen'] = x.findNextSibling('td').string
                    elif 'hoeveelheid' in x.string:
                        gc.properties['Geheugengrootte'] = x.findNextSibling('td').string
                    elif 'geheugentype' in x.string:
                        gc.properties['GeheugenType'] = x.findNextSibling('td').string
                    elif 'Geheugen kloksnelheid' in x.string:
                        gc.properties['GeheugenSnelheid'] = x.findNextSibling('td').string
                    elif 'bandbreedte' in x.string:
                        gc.properties['GeheugenBusbreedte'] = x.findNextSibling('td').string
                    elif 'Bus type' in x.string:
                        gc.properties['CardInterface'] = x.findNextSibling('td').string
                    elif 'DirectX' in x.string:
                        gc.properties['DirectXversion'] = x.findNextSibling('td').string
                    elif 'OpenGL' in x.string:
                        gc.properties['OpenGLversion'] = x.findNextSibling('td').string
                    elif 'sloten' in x.string:
                        gc.properties['aantalSlots'] = x.findNextSibling('td').string

        voorraad = IParseSave.voorraadChecker(detailadress)
        IParseSave.saveComponent(gc.properties, label, price,voorraad,detailadress, winkel)


class Motherboard(IParseSave.Motherboard):
    def motherBoardParser(detailadress):
        label = 'Motherboard'
        mb = Motherboard()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})

        product = soup.find('h1')
        product = product.string
        splitStrings = product.split(',')
        mb.properties['product'] = splitStrings[0]

        brand = soup.find('span', {'itemprop': 'brand'})
        mb.properties['Merk'] = brand.string

        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace('.', '')
        price = price.replace(',', '.')
        price = float(price[2:])

        mb.properties['Img'] = IParseSave.imgFinder(detailadress)

        breadCrumbvariables = soup.findAll('span', {'itemprop': 'title'})
        for x in breadCrumbvariables:
            if 'Socket' in x.string:
                mb.properties['socket'] = x.string

        if specs is not None:
            for x in specs:
                if x.string is not None:
                    if 'Fabrikantcode' in x.string:
                        mb.properties['ModelID'] = x.findNextSibling('td').string
                    if 'geheugensloten' in x.string:
                        mb.properties['AantalSockets'] = x.findNextSibling('td').string
                    elif 'Form factor' in x.string:
                        mb.properties['FormFactor'] = x.findNextSibling('td').string
                    elif 'Chipset' in x.string:
                        mb.properties['Moederbordchipset'] = x.findNextSibling('td').string
                    elif 'Type geheugen' in x.string:
                        mb.properties['Geheugentype'] = x.findNextSibling('td').string
                    elif 'PCI-E x16 sloten' in x.string:
                        mb.properties['AantalPCI-ex16Slots'] = x.findNextSibling('td').string

        voorraad = IParseSave.voorraadChecker(detailadress)
        IParseSave.saveComponent(mb.properties, label, price,voorraad, detailadress, winkel)


class RAM(IParseSave.RAM):
    def RAMparser(detailadress):
        label = 'RAM'
        ram = RAM()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})

        product = soup.find('h1')
        product = product.string
        splitStrings = product.split(',')
        ram.properties['Name'] = splitStrings[0]

        brand = soup.find('span', {'itemprop': 'brand'})
        ram.properties['Merk'] = brand.string

        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace('.', '')
        price = price.replace(',', '.')
        price = float(price[2:])

        ram.properties['Img'] = IParseSave.imgFinder(detailadress)

        type = soup.findAll('span', {'itemprop': 'title'})
        for x in type:
            if 'DDR' in x.string:
                type = x.string
                type = type[:4]
                ram.properties['GeheugenType'] = type


        if specs is not None:
            for x in specs:
                if x.string is not None:
                    if 'Fabrikantcode' in x.string:
                        ram.properties['ModelID'] = x.findNextSibling('td').string
                    if 'capactiteit' in x.string:
                        ram.properties['GeheugenSpecificatie'] = x.findNextSibling('td').string
                    elif 'modules' in x.string:
                        ram.properties['Aantal'] = x.findNextSibling('td').string
                    elif 'Latency' in x.string:
                        ram.properties['GeheugenCASLatency'] = x.findNextSibling('td').string

        voorraad = IParseSave.voorraadChecker(detailadress)
        IParseSave.saveComponent(ram.properties, label, price,voorraad,detailadress, winkel)


class Storage(IParseSave.Storage):
    def storageParser(detailadress):
        label = 'Storage'
        store = Storage()
        soup = getHTML(detailadress)
        specs = soup.findAll('td', {'class': 'right'})

        product = soup.find('h1')
        product = product.string
        store.properties['product'] = product

        brand = soup.find('span', {'itemprop': 'brand'})
        store.properties['Merk'] = brand.string

        price = soup.find('p', {'class': 'verkoopprijs'})
        price = price.string
        price = price.replace('.', '')
        price = price.replace(',', '.')
        price = float(price[2:])

        store.properties['Img'] = IParseSave.imgFinder(detailadress)

        if specs is not None:
            for x in specs:
                if x.string is not None:
                    if 'Fabrikantcode' in x.string:
                        store.properties['ModelID'] = x.findNextSibling('td').string
                    if 'Capaciteit' in x.string:
                        store.properties['Opslagcapactiteit'] = x.findNextSibling('td').string
                    if 'Dikte' in x.string:
                        store.properties['Hoogte'] = x.findNextSibling('td').string
                    if 'Rotatiesnelheid' in x.string:
                        store.properties['RotatieSnelheid'] = x.findNextSibling('td').string
                    if 'Chache' in x.string:
                        store.properties['DriveCache'] = x.findNextSibling('td').string

        voorraad = IParseSave.voorraadChecker(detailadress)

        IParseSave.saveComponent(store.properties, label, price, voorraad, detailadress, winkel)


graph = Graph("http://localhost:7484/db/data/")
winkel = Node('Store', Name='informatique.nl')
graph.create(winkel)

topLevelSpider('http://www.informatique.nl/componenten/', getCategories())
