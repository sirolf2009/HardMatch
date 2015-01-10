#!/usr/bin/env python
#coding: utf8

__author__ = 'Basit'


import requests
from bs4 import BeautifulSoup
from py2neo import Node, Relationship, Graph


def getHTML(url):
    # print(url)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup


def printProperties(properties):
    for x in properties:
        print(x)
        print(properties[x])


def saveComponent(properties, winkel, label, price):
    cn = Node(label)
    winkel.pull()
    for i in properties:
        cn.properties[i] = properties[i]
    graph = Graph("http://localhost:7484/db/data/")
    rel = Relationship(cn, 'SOLD_AT', winkel, price=price)
    graph.create(cn)
    graph.create(rel)
    cn.add_labels('Component')
    cn.push()


class CPU():
    properties = {
        'modelID': 'null',
        'name': 'null',
        'brand': 'null',
        'serie': 'null',
        'product': 'null',  # eerste gedeelte van de productnaam
        'Socket': 'null',
        'AantalCores': 'null',
        'Snelheid': 'null',
        'ThermalDesignPower': 'null',
        'CPUSSpecNumber': 'null',
        'MaximaleTurboFrequentie': 'null',
        'GeheugenSpecificatie': 'null',
        'BusSnelheid': 'null',
        'Procestechnologie': 'null',
        'GeïntegreerdeGraphics': 'null',
        'Gpu': 'null',
        'NominaleSnelheidVideochip': 'null',
        'MaximaleSnelheidVideochip': 'null',
        'CPUCacheLevel1': 'null',
        'CPUCacheLevel2': 'null',
        'CPUCacheLevel3': 'null',
        'Threads': 'null',
        'Virtualisatie': 'null',
        'VirtualisatieType':'null',
        'CPUMultiplier': 'null',
        'CPUStepping': 'null',
        'CPUInstructieset ': 'null',
        'TypeKoeling': 'null'
    }


class GraphicsCard():
    properties = {
        'modelID': 'null',
        'brand': 'null',
        'product': 'null',
        'Videochip': 'null',  # GeForce GTX 970
        'ChipsetGeneratie': 'null',  # GeForce 900 Serie
        'Videochipfabrikant': 'null',  # Nvidia
        'NominaleSnelheidVideochip': 'null',
        'MaximaleTurboFrequentie': 'null',
        'Rekenkernen': 'null',  # 1.664
        'Geheugengrootte': 'null',  # 4GB
        'GeheugenType': 'null',  # GDDR5
        'GeheugenSnelheid': 'null',  # 7,01GHz
        'GeheugenBusbreedte': 'null',  # 256 bit
        'CardInterface': 'null',  # PCI-e 3.0 x16
        'VideoUit': 'null',  # DVI-D, DVI-I, HDMI
        'HoogsteHDMIVersie': 'null',  # HDMI 2.0
        'HoogsteDisplayPortVersie': 'null',  # DisplayPort 1.2
        'VideoAdapter': 'null',  # DVI naar D-Sub adapter
        'DirectXversion': 'null',  # 12.0
        'OpenGLversion': 'null',  # 4.4
        'ShaderModel': 'null',  # 5.0
        'MaximaleResolutie': 'null',  # 4096x2160 (Cinema 4K)
        'Lengte': 'null',  # 269mm
        'Hoogte': 'null',  # 35mm
        'Breedte': 'null',  # 141mm
        'AantalSlots': 'null',  # 2x
        'AantalPins': 'null',
        'Aantal6Pins': 'null',  # 1x
        'Aantal8Pins': 'null',  # 1x
        'Stroomverbruik': 'null',  # 148W
        'TypeKoeling': 'null',  # Passieve fan
        'linkInterface': 'null'  # Nvidia SLi
    }



class Motherboard():
    properties = {
        'modelID': 'null',
        'brand': 'null',
        'product': 'null',  # Asus M5A78L-M
        'socket': 'null',
        'AantalSockets': 'null',
        'FormFactor': 'null',
        'BIOSofUEFI': 'null',
        'DualofSingleBIOSUEFI': 'null',
        'Moederbordchipset': 'null',
        'Geheugentype': 'null',
        'MaximumGeheugengrootte': 'null',
        'HardeschijfBus': 'null',
        'CardInterface': 'null',
        'AantalPCI-ex16Slots': 'null',
        'LinkInterfaceATiCrossfireATiCrossfire': 'null',
        'VerbindingEthernet': 'null',
        'Netwerkchip': 'null',
        'BluetoothAanwezig': 'null',
        'VerbindingUSBFW': 'null',
        'VideoUit': 'null',
        'Verbinding': 'null',
        'AudioKanalen': 'null',
        'AudioUitgangen': 'null',
        'Audiochip': 'null'
    }


class RAM():
    properties = {
        'modelID': 'null',
        'brand': 'null',  # Crucial
        'serie': 'null',  # Ballistix
        'Geheugengrootte': 'null',  #8GB
        'Aantal': 'null',  #2x
        'Modulegrootte': 'null',  #4GB
        'GeheugenType': 'null',  #DDR3
        'GeheugenSpecificatie': 'null',  #PC3-12800 (DDR3-1600)
        'LowVoltageDDR': 'null',  #Nee
        'GeheugenCASLatency': 'null',
    }



class Storage():
    properties = {
        'modelID': 'null',
        'brand': 'null',  # WD
        'serie': 'null',  # Red
        'product': 'null',  #WD Red SATA 6 Gb/s
        'Opslagcapactiteit': 'null',  #3TB
        'HardeschijfBusIntern': 'null',  #SATA-600
        'Hoogte': 'null',  #26,1mm
        'Lezen':'null',
        'Schrijven':'null',
        'RotatieSnelheid': 'null',  #5.400
        'DriveCache': 'null',  #64MB
        'CommandQueuing': 'null',  #Native Command Queuing
        'ReadSeekTime':'null',
        'StroomverbruikLezen': 'null',  #4,5W
        'StroomverbruikSchrijven': 'null',  #4,5W
    }


def printProperties(properties):
    for x in properties:
        print(x)
        print(properties[x])
