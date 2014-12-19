__author__ = 'Basit'

import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, Node, Relationship, Graph

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
            motherBoardParser(link)
        elif label == 'Processor':
            cpuParser(link)
        elif label == 'Graphics card':
            graphicsCardParser(link)
        elif label == 'RAM':
            RAMparser(link)
        elif label == 'Storage':
            storageParser(link)
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

class CPU():
    properties = {
        'label': 'CPU',
        'name': 'null',
        'price': 'null',
        'brand': 'null',
        'serie': 'null',
        'product': 'null',  # eerste gedeelte van de productnaam
        'socket': 'null',
        'amountOfCores': 'null',
        'speed': 'null',
        'thermalDesignPower': 'null',
        'CPUsSpecNumber': 'null',
        'maxiTurboFrequency': 'null',
        'memorySpecification': 'null',
        'busSpeed': 'null',
        'procesTechnology': 'null',
        'intergratedGraphics': 'null',
        'gpu': 'null',
        'nominalSpeedVideochip': 'null',
        'maxSpeedVideochip': 'null',
        'CPUCacheLevel1': 'null',
        'CPUCacheLevel2': 'null',
        'CPUCacheLevel3': 'null',
        'threads': 'null',
        'virtualisation': 'null',
        'CPUMultiplier': 'null',
        'CPUStepping': 'null',
        'CPUInstructionSet': 'null',
        'typeCooling': 'null',
        'guarantee': 'null',
        'EAN': 'null',
        'SKU': 'null'
    }


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

    saveComponent(cpu.properties)


class GraphicsCard():
    properties = {
        'label': 'GraphicsCard',
        'brand': 'null',
        'product': 'null',
        'price': 'null',
        'videochip': 'null',  # GeForce GTX 970
        'chipsetGeneration': 'null',  # GeForce 900 Serie
        'videochipManufacturer': 'null',  # Nvidia
        'nominalSpeedVideochip': 'null',
        'maxiTurboFrequency': 'null',
        'calculatingCores': 'null',  # 1.664
        'memoryCapacity': 'null',  # 4GB
        'memoryType': 'null',  # GDDR5
        'memorySpeed': 'null',  # 7,01GHz
        'memoryBusWidth': 'null',  # 256 bit
        'cardInterface': 'null',  # PCI-e 3.0 x16
        'videoOutDisplayPort': 'null',  # DVI-D, DVI-I, HDMI
        'highestHDMIVersion': 'null',  # HDMI 2.0
        'highestDisplayPortVersion': 'null',  # DisplayPort 1.2
        'videoAdapter': 'null',  # DVI naar D-Sub adapter
        'directXversion': 'null',  # 12.0
        'openGLversion': 'null',  # 4.4
        'shaderModel': 'null',  # 5.0
        'maxResolution': 'null',  # 4096x2160 (Cinema 4K)
        'length': 'null',  # 269mm
        'height': 'null',  # 35mm
        'width': 'null',  # 141mm
        'amountOfSlots': 'null',  # 2x
        'amountOf6Pins': 'null',  # 1x
        'amountOf8Pins': 'null',  # 1x
        'energyUsage': 'null',  # 148W
        'typeCooling': 'null',  # Passieve fan
        'linkInterface': 'null',  # Nvidia SLi
        'EAN': 'null',  # 4719072365752
        'SKU': 'null'  # GTX 970 GAMING 4G, V316-001R
    }


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

    saveComponent(gc.properties)

class Motherboard():
    properties = {
        'label': 'Motherboard',
        'brand': 'null',
        'serie': 'null',  # AMD AM3+
        'product': 'null',  # Asus M5A78L-M
        'price': 'null',
        'socket': 'null',  #AM3+
        'amountOfSockets': 'null',
        'maxTDPprocessor': 'null',  #140W
        'formFactor': 'null',  #Micro-ATX (µATX)
        'BIOSorUEFI': 'null',  #BIOS
        'dualorSingleBIOSUEFI': 'null',  #Single
        'motherboardChipset': 'null',  #AMD 760G
        'memoryType': 'null',  #4x DDR3
        'maxMemoryCapacity': 'null',  # GB
        'HDDbus': 'null',  #6x SATA-300
        'raidModi': 'null',  #0, 1, 1E, 10, JBOD
        'cardInterface': 'null',  #2x PCI, PCI-e x1, PCI-e x16
        'amountOfPCIex16slots': 'null',
        'linkInterface': 'null',  # ATi Crossfire
        'ethernetConnection': 'null',  #Ethernet 1Gbps
        'networkchip': 'null',  #Realtek RTL8111E
        'bluetooth': 'null',  #Nee
        'USBFWConnection': 'null',  #10x USB 2.0, 2x USB 3.0
        'videoOutput': 'null',  #(VGA), DVI-D, HDMI
        'otherConnections': 'null',  #PS/2
        'audioChannels': 'null',  #8 (7.1)
        'audioOutputAnalog': 'null',  #(3,5mm)
        'audioOutputDigital': 'null',  #Digitaal Optisch (S/PDIF)
        'audioChip': 'null',  #VIA VT1708S
        'EAN': 'null',
        #0610839181117, 4016138700787, 4054317892960, 4719543181119, 5053086113800, 5053460703757, 5053460854701, 5711045802461, 6108391811176
        'SKU': 'null'  #90-MIBG70-G0EAY00Z, 90-MIBG70-G0EAY0GZ, M5A78L-M/USB3
    }

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

    saveComponent(mb.properties)


class RAM():
    properties = {
        'label': 'RAM',
        'brand': 'null',  # Crucial
        'serie': 'null',  #Ballistix
        'price': 'null',
        'memoryCapacity': 'null',  #8GB
        'amount': 'null',  #2x
        'moduleCapacity': 'null',  #4GB
        'pricePerGB': 'null',  #7,869
        'memoryType': 'null',  #DDR3
        'memorySpecification': 'null',  #PC3-12800 (DDR3-1600)
        'lowVoltageDDR': 'null',  #Nee
        'memoryCASLatency': 'null',
        'voltage': 'null',  #1,5V
        'manufacturerGuarantee': 'null',  #Levenslang
        'EAN': 'null',  #0649528755940
        'SKU': 'null'  #BLS2CP4G3D1609DS1S00, BLS2CP4G3D1609DS1S00CEU
    }

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

    saveComponent(ram.properties)


class Storage():
    properties = {
        'label': 'Storage',
        'brand': 'null',  # WD
        'serie': 'null',  #Red
        'product': 'null',  #WD Red SATA 6 Gb/s
        'price': 'null',
        'memoryCapacity': 'null',  #3TB
        'storageBus': 'null',  #SATA-600
        'caseBay': 'null',  #3.5"
        'height': 'null',  #26,1mm
        'rotationSpeed': 'null',  #5.400
        'driveCache': 'null',  #64MB
        'commandQueuing': 'null',  #Native Command Queuing
        'powerUsageRead': 'null',  #4,5W
        'powerUsageWrite': 'null',  #4,5W
        'pricePerGB': 'null',  #0,036
        'manufacturerGuarantee': 'null',  #3 jaar carry in
        'EAN': 'null',  #0718037799674, 5711045474873
        'SKU': 'null'  #WD30EFRX
    }

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

    saveComponent(store.properties)

def printProperties(properties):
    for x in properties:
        print(x)
        print(properties[x])

def saveComponent(properties):
        cn = Node(properties['label'])
        winkel.pull()
        for i in properties:
            cn.properties[i] = properties[i]
        graph = Graph("http://localhost:7474/db/data/")
        rel = Relationship(cn, 'Sold at', winkel, price=properties['price'])
        graph.create(cn)
        graph.create(rel)

#cpu = cpuParser('http://www.informatique.nl/539941/intel-core-i5-4460-3-2ghz-6mb-s1150.html?spcall=yes')
#graphicsCard = graphicsCardParser('http://www.informatique.nl/543790/msi-geforce-gtx-970-4gb-gaming.html?spcall=yes')
#motherBoard = motherBoardParser('http://www.informatique.nl/201163/gigabyte-ga-x79-ud3.html?spcall=yes')
#ram = RAMparser('http://www.informatique.nl/543398/crucial-ct4g4dfs8213.html?spcall=yes')
#printProperties(cpu)
#printProperties(graphicsCard)
#printProperties(motherBoard)
#printProperties(ram)
#store = storageParser('http://www.informatique.nl/561673/samsung-840-evo-250gb.html?spcall=yes')
#printProperties(store)

graph = Graph("http://localhost:7474/db/data/")
winkel = Node('Store', Naam='informatique.nl')
graph.create(winkel)
topLevelSpider('http://www.informatique.nl/componenten/', getCategories())