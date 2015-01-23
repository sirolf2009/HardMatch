#!/usr/bin/env python
#coding: utf8

__author__ = 'Basit'


import time
import datetime
import requests
from bs4 import BeautifulSoup
from py2neo import Node, Relationship, Graph, neo4j, schema
import pymongo



def getHTML(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup

def imgFinder(link):
    soup = getHTML(link)
    img = soup.find('img', {'class':'full'})
    imgLink = img.get('src')
    return imgLink

def cardInterfaceBuilder(link):
    soup = getHTML(link)
    specs = soup.findAll('td',{'class': 'right'})

    dict = {
        'interfaces': ''
    }

    if specs is not None:
        for x in specs:
            if x.string is not None:
                if 'PCI' in x.string:
                    rawValue = x.string
                    roughValue = rawValue.split(' ')
                    roughValue = roughValue[1]
                    dict['interfaces'] += ' '+ roughValue + ' ' + x.findNextSibling('td').string.replace(' ','')
            else:
                return None

        return(dict['interfaces'])


def printProperties(properties):
    for x in properties:
        print(x)
        print(properties[x])

def voorraadChecker(url):
    soup = getHTML(url)
    voorraad = 'Niet op voorraad'
    substring = 'Online op voorraad'
    for x in soup.find('td', {'style': 'padding:5px 4px 5px 4px;line-height:2'}):
        if x is not None:
            if substring in x:
                voorraad = 'Op voorraad'
    return voorraad

def saveComponent(properties, label, price, voorraad,link, winkel):
    graph = Graph("http://localhost:7484/db/data/")
    modelID = properties['ModelID']

    if bool(graph.cypher.execute_one('match (n) where n.ModelID = "{}" return n'.format(modelID))):
        cn = graph.cypher.execute_one('match (n) where n.ModelID = "{}" return n'.format(modelID))
    else:
        cn = Node(label)
        for i in properties:
            cn.properties[i] = properties[i]
        graph.create(cn)
        cn.add_labels('Component')
        cn.push()

    rel = Relationship(cn, 'SOLD_AT', winkel, Price=price, inStock=voorraad, productUrl=link)
    graph.create(rel)
    saveMetaData(winkel.properties['Name'], properties['Name'], modelID, price, properties['Merk'],'www.Informatique.nl', label)
    time.sleep(3)


def saveMetaData(dbname,productName, modelID, price, merk, store, label):
    try:
        client = pymongo.MongoClient()

        if dbname == 'www.informatique.nl':
            db = client.informatique
        else:
            db = client.alternate

        now = datetime.datetime.now()
        metadata = {
            'Store': store,
            'ModelID': '(Fabrikantcode('+modelID+')',
            'Name': productName,
            'Price': price,
            'Brand': merk,
            'productType': label,
            'Timestamp': int(time.mktime(now.timetuple()))
        }

        #determine the right collection to insert the post in to
        if label == 'CPU': collection = db.CPU
        elif label == 'Motherboard': collection = db.Motherboard
        elif label == 'CPUFan': collection = db.CPUFan
        elif label == 'GraphicsCard': collection = db.GraphicsCard
        elif label == 'RAM': collection = db.RAM
        elif label == 'Case': collection = db.Case
        elif label == 'PSU': collection =db.PSU
        elif label == 'Barebones':collection = db.Barebones
        elif label == 'Storage-HDD':collection = db.HDD
        elif label == 'Storage-SSD': collection =db.SSD
        elif label == 'Storage': collection =db.Storage
        else: collection = db.MISC

        collection.insert(metadata)
    except pymongo.errors.ConnectionFailure:
        print('No connection could be made with MongoDB')


class CPU():
    properties = {
        'ModelID': 'NULL',
        'Name': 'NULL',
        'Merk': 'NULL',
        'Serie': 'NULL',
        'Socket': 'NULL',
        'AantalCores': 'NULL',
        'Snelheid': 'NULL',
        'ThermalDesignPower': 'NULL',
        'CPUSSpecNumber': 'NULL',
        'MaximaleTurboFrequentie': 'NULL',
        'GeheugenSpecificatie': 'NULL',
        'BusSnelheid': 'NULL',
        'Procestechnologie': 'NULL',
        'GeïntegreerdeGraphics': 'NULL',
        'Gpu': 'NULL',
        'NominaleSnelheidVideochip': 'NULL',
        'MaximaleSnelheidVideochip': 'NULL',
        'CPUCacheLevel1': 'NULL',
        'CPUCacheLevel2': 'NULL',
        'CPUCacheLevel3': 'NULL',
        'Threads': 'NULL',
        'Virtualisatie': 'NULL',
        'VirtualisatieType':'NULL',
        'CPUMultiplier': 'NULL',
        'CPUStepping': 'NULL',
        'CPUInstructieset ': 'NULL',
        'TypeKoeling': 'NULL'
    }


class CPUFan():
    properties = {
        'img': 'NULL',
        'ModelID': 'NULL',
        'Name': 'NULL',
        'Merk': 'NULL',
        'Serie': 'NULL',
        'Socket': 'NULL'
    }


class Case():
    properties = {
        'img': 'NULL',
        'ModelID': 'NULL',
        'Name': 'NULL',
        'Merk': 'NULL',
        'Serie': 'NULL',
        'FormFactor': 'NULL',
        'VoedingFormFactor': 'NULL'
    }


class GraphicsCard():
    properties = {
        'ModelID': 'NULL',
        'Merk': 'NULL',
        'Name': 'NULL',
        'Videochip': 'NULL',  # GeForce GTX 970
        'ChipsetGeneratie': 'NULL',  # GeForce 900 Serie
        'Videochipfabrikant': 'NULL',  # Nvidia
        'NominaleSnelheidVideochip': 'NULL',
        'MaximaleTurboFrequentie': 'NULL',
        'Rekenkernen': 'NULL',  # 1.664
        'Geheugengrootte': 'NULL',  # 4GB
        'GeheugenType': 'NULL',  # GDDR5
        'GeheugenSnelheid': 'NULL',  # 7,01GHz
        'GeheugenBusbreedte': 'NULL',  # 256 bit
        'CardInterface': 'NULL',  # PCI-e 3.0 x16
        'VideoUit': 'NULL',  # DVI-D, DVI-I, HDMI
        'HoogsteHDMIVersie': 'NULL',  # HDMI 2.0
        'HoogsteDisplayPortVersie': 'NULL',  # DisplayPort 1.2
        'VideoAdapter': 'NULL',  # DVI naar D-Sub adapter
        'DirectXVersie': 'NULL',  # 12.0
        'OpenGLVersie': 'NULL',  # 4.4
        'ShaderModel': 'NULL',  # 5.0
        'MaximaleResolutie': 'NULL',  # 4096x2160 (Cinema 4K)
        'Lengte': 'NULL',  # 269mm
        'Hoogte': 'NULL',  # 35mm
        'Breedte': 'NULL',  # 141mm
        'AantalSlots': 'NULL',  # 2x
        'AantalPins': 'NULL',
        'Aantal6Pins': 'NULL',  # 1x
        'Aantal8Pins': 'NULL',  # 1x
        'Stroomverbruik': 'NULL',  # 148W
        'TypeKoeling': 'NULL',  # Passieve fan
        'linkInterface': 'NULL'  # Nvidia SLi
    }


class Motherboard():
    properties = {
        'ModelID': 'NULL',
        'Merk': 'NULL',
        'Name': 'NULL',  # Asus M5A78L-M
        'Socket': 'NULL',
        'AantalSockets': 'NULL',
        'FormFactor': 'NULL',
        'BIOSofUEFI': 'NULL',
        'DualofSingleBIOSUEFI': 'NULL',
        'Moederbordchipset': 'NULL',
        'Geheugentype': 'NULL',
        'MaximumGeheugengrootte': 'NULL',
        'HardeschijfBus': 'NULL',
        'CardInterface': 'NULL',
        'AantalPCI-ex16Slots': 'NULL',
        'LinkInterfaceATiCrossfireATiCrossfire ': 'NULL',
        'VerbindingEthernet': 'NULL',
        'Netwerkchip': 'NULL',
        'BluetoothAanwezig': 'NULL',
        'VerbindingUSBFW': 'NULL',
        'VideoUit': 'NULL',
        'Verbinding': 'NULL',
        'AudioKanalen': 'NULL',
        'AudioUitgangen': 'NULL',
        'Audiochip': 'NULL'
    }


class RAM():
    properties = {
        'ModelID': 'NULL',
        'Merk': 'NULL',  # Crucial
        'Name': 'NULL',
        'serie': 'NULL',  # Ballistix
        'Geheugengrootte': 'NULL',  #8GB
        'Aantal': 'NULL',  #2x
        'Modulegrootte': 'NULL',  #4GB
        'GeheugenType': 'NULL',  #DDR3
        'GeheugenSpecificatie': 'NULL',  #PC3-12800 (DDR3-1600)
        'LowVoltageDDR': 'NULL',  #Nee
        'GeheugenCASLatency': 'NULL',
    }


class Storage():
    properties = {
        'ModelID': 'NULL',
        'Merk': 'NULL',  # WD
        'serie': 'NULL',  # Red
        'Name': 'NULL',  #WD Red SATA 6 Gb/s
        'Opslagcapactiteit': 'NULL',  #3TB
        'HardeschijfBusIntern': 'NULL',  #SATA-600
        'Hoogte': 'NULL',  #26,1mm
        'Lezen':'NULL',
        'Schrijven':'NULL',
        'RotatieSnelheid': 'NULL',  #5.400
        'DriveCache': 'NULL',  #64MB
        'CommandQueuing': 'NULL',  #Native Command Queuing
        'ReadSeekTime':'NULL',
        'StroomverbruikLezen': 'NULL',  #4,5W
        'StroomverbruikSchrijven': 'NULL',  #4,5W
    }


def printProperties(properties):
    for x in properties:
        print(x)
        print(properties[x])

