#!/usr/bin/python
__author__ = 'gokhankacan'
import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, Node, Relationship, Graph
from pymongo import MongoClient, Connection
from datetime import datetime
import time
import threading as t
from queue import Queue

# Static Value(s) voor the System
class Statistic: productCount = 0
db = Graph("http://localhost:7474/db/data/")

# Mongo Client Connection
client = MongoClient('localhost', 27017)
mongodb = client.coolblue

subCategoriesQueue = Queue()

def main():
    categorieLevel('coolblue')


def stores(store):

    if store == 'informatique':
        link = 'www.informatique.nl'
    elif store == 'alternate':
        link = 'www.alernate.nl'
    elif store == 'azerty':
        link = 'www.azerty.nl'
    elif store == 'coolblue':
        link = 'http://www.processorstore.nl/category/212272/pc-componenten.html'
    elif store == 'mediamarkt':
        link = 'www.mediamarkt.nl'
    else:
        link = 'Geen juiste winkel gekozen'

    return link



def soup_function(args):
    source = requests.get(args)
    plain = source.text
    soup = BeautifulSoup(plain)
    return soup




def categorieLevel(storeURL):

    start = True

    while start:
        soup = soup_function(stores(storeURL))

        for categories in soup.findAll('a', {'class': 'facetAction'}):

            # componentCategorie = categories.get('title')
            href = 'http://www.processorstore.nl' + categories.get('href')
            subCategoriesQueue.put(href)
            start = False

        # print(subCategoriesQueue.empty())
        print(subCategoriesQueue.qsize())

    threadSubs(subCategoriesQueue)
    # productListingPages(subCategoriesQueue)


"""
def categorieLevel(storeURL):

    start = True
    subCategoriesArray = []
    # subCategoriesQueue = Queue()

    while start:
        soup = soup_function(stores(storeURL))

        for categories in soup.findAll('a', {'class': 'facetAction'}):

            # componentCategorie = categories.get('title')
            href = 'http://www.processorstore.nl' + categories.get('href')
            subCategoriesArray.append(href)
            start = False

    productListingPages(subCategoriesArray)
"""




def threadSubs(subCategoriesQueue):


    while subCategoriesQueue.empty() == False:

        for i in range(0, subCategoriesQueue.qsize()):

            i = t.Thread(target=productListingPages(), name="SubcategoriesThreading")
            i.daemon = True
            i.start()


def productListingPages():

        subUrl = subCategoriesQueue.get()  # Get url from Queue
        soup = soup_function(subUrl)    # Make a soup Object
        componentTitle = soup.find('h1', {'class': 'specification-filter-head'}).text  # Check which component category it belongs to

        # Check Maximum Pagenumbers
        subCategoriePages = soup.findAll('li', {'class': 'paging-navigation-last-page'})[0]
        maxPageNumbers = subCategoriePages.text.strip()

        productListingLevel(int(maxPageNumbers), subUrl, componentTitle)
        subUrl.task_done()




"""
def productListingPages(subCategoriesQueue):

    for index in subCategoriesQueue:

        categorie_url = index
        if categorie_url == "http://www.processorstore.nl/category/212284/upgrade-kits.html": break
        elif categorie_url == "http://www.processorstore.nl/category/212742/pci-kaarten.html": break
        elif categorie_url == "http://www.processorstore.nl/category/212880/branders-dvd-blu-ray.html": break
        else:

            # Make a soup Object
            soup = soup_function(categorie_url)

            # Check which component category it belongs to
            componentTitle = soup.find('h1', {'class': 'specification-filter-head'}).text

            # Check Maximum Pagenumbers
            subCategoriePages = soup.findAll('li', {'class': 'paging-navigation-last-page'})[0]
            maxPageNumbers = subCategoriePages.text.strip()

            productListingLevel(int(maxPageNumbers), categorie_url, componentTitle)
"""



def productListingLevel(max_pages, URL, componentTitle):
    page = 1

    while page <= max_pages:
        soup = soup_function(URL + '?sort=popularity&dir=d&page=' + str(page))

        for product in soup.findAll('li', {'class': 'product-list-columns--item product-list-item'}):

            priceTag = product.select('div.product-list-item--order-information > div.product-list-item--priceinformation > strong.product-list-item--price')
            priceStr = priceTag[0].text.strip()
            price = float(priceStr.replace(',', '.').replace('-', '00'))


            info = product.select('h2.product-list-item--title a')
            href = 'http://www.processorstore.nl' + info[0].get('href')
            title = info[0].string

            # time.sleep(2)

            print(title, href, price, componentTitle)
            productPageLevel(title, href, price, componentTitle)

        page += 1

    print('Finished Completeeeeee!')





def productPageLevel(title, href, price, componentTitle):

    # Database Connect
    # db = Graph("http://localhost:7484/db/data/")


    # CREATE STORE NODE
    # If Node exists in Database then Pass ELSE Create Store Node
    if bool(db.cypher.execute_one('MATCH(n:Store) WHERE n.Name = "www.processorstore.nl" RETURN n')):
        pass
    else:
        store = storeObject.createStore('Store', 'Store', 'ProcessorStore', 'Weena 664', '3012 CN', 'Rotterdam', 'www.processorstore.nl', '010-7988999')  # Setup Store Node (Coolblue)
        db.create(store)
    store = db.cypher.execute_one('MATCH(n:Store) WHERE n.Name = "www.processorstore.nl" RETURN n')


    # Make BS4 Object
    soup = soup_function(href)


    # Create Product Specs Dictionary
    PD = {}

    # Get Interface & set NULL by ComponentType
    p = interface(componentTitle)

    # Dictionary CPUs'
    cpuCores = {'Single-core': '1', 'Dual-core': '2', 'Quad-core': '4', 'Octa-core': '8', '6-Core': '6', '8-Core': '8'}
    productType = {'Processoren': 'CPU', 'Moederborden': 'Motherboard', 'Processorkoelers en Koelpasta': 'CPUFan', 'Videokaarten': 'GraphicsCard', 'RAM-geheugen': 'RAM', 'Computerbehuizingen': 'Case', 'SSD (Solid State Drive)': 'Storage-SSD', 'Interne harde schijven (HDD)': 'Storage-HDD', 'Voedingen (PSU)': 'PSU', 'Geluidskaarten': 'Soundcard', 'Barebones': 'Barebones'}


    # Check Stock of Product
    stockTag = soup.select('div.availability-state > span.availability-state--title')
    stock = stockTag[0].get_text(strip=True)

    imgTag = soup.find('img', {'itemprop': 'image'})
    # imgTag.get('src')

    # Statistic Product Count
    Statistic.productCount += 1

    # IMPORTANT!: Saving Fabrikantcode AS ModelID
    for dt in soup.findAll('dt', {'class': 'product-specs--item-title'}):
        dd = dt.find_next_sibling("dd", {'class': 'product-specs--item-spec'})
        if dt.text.strip() in ['Fabrikantcode', 'Artikelnummer', 'Merk', 'Garantie', 'Garantietype']:
            PD[dt.text.strip()] = dd.text.strip()


    # IF ModelID a.k.a. Fabrikantcode Exists TRUE/FALSE
    if bool(db.cypher.execute('MATCH (n) WHERE n.ModelID = "{}" RETURN n'.format(PD['Fabrikantcode']))) == False:


        # Loop Through All Values in Product Specifications
        for spec in soup.select('div.product-specs dl.product-specs--list > dt.product-specs--item-title span.product-specs--help-title'):

            parent = spec.find_parent('dt')
            value = parent.find_next_sibling("dd", {'class': 'product-specs--item-spec'})
            # print(spec.get_text(strip=True), ': ', value.text.strip())

            # Add Additional Key & Value to Dictionary
            PD[spec.get_text(strip=True)] = value.text.strip()


            if componentTitle == 'Processoren':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Serie': p["Serie"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Socket': p['Socket'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Garantie': p["Garantie"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Garantietype': p["Garantietype"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Processorkernen': p["AantalCores"] = cpuCores[value.text.strip()]
                    elif spec.get_text(strip=True) == 'Kloksnelheid': p['Snelheid'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Turbo Frequency': p['MaximaleTurboFrequentie'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Geheugencontroller': p['GeheugenSpecificatie'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Productieproces': p['Procestechnologie'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Stroomverbruik maximaal': p['ThermalDesignPower'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Cache': p['CPUCacheLevel3'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Threads': p['Threads'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Multiplier unlocked': p['CPUMultiplier'] = value.text.strip()

                    product = productNode.nodeCPU('CPU', p['img'], p['Socket'], p['ModelID'], p['Serie'], p['Name'], p['Merk'], p['Garantie'], p['Garantietype'], p['AantalCores'],p['CPUSSpecNumber'],p['Snelheid'],p['MaximaleTurboFrequentie'], p['GeheugenSpecificatie'],p['BusSnelheid'],p['Procestechnologie'],p['ThermalDesignPower'],p['GeïntegreerdeGraphics'],p['Gpu'],p['NominaleSnelheidVideochip'],p['MaximaleSnelheidVideochip'],p['CPUCacheLevel1'],p['CPUCacheLevel2'],p['CPUCacheLevel3'],p['Threads'],p['Virtualisatie'],p['VirtualisatieType'],p['CPUMultiplier'],p['CPUstepping'], p['CPUInstructieset'], p['TypeKoeling'])
                else: pass



            elif componentTitle == 'Moederborden':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Formaat moederbord': p["FormFactor"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Socket': p["Socket"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Maximale hoeveelheid geheugen': p["MaximumGeheugengrootte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Geheugen': p["Geheugentype"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'PCI Express x16-sloten': p["AantalPCIex16Slots"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Ethernetpoorten': p["VerbindingEthernet"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Bluetooth': p["BluetoothAanwezig"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Aantal USB 2.0-poorten': p["VerbindingUSBFW"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Audio processor': p["Audiochip"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'VGA-poort': p["VideoUit"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'UEFI BIOS': p["BIOSofUEFI"] = value.text.strip()
                    product = productNode.nodeMotherboard('Motherboard', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Socket'], p['AantalSockets'], p['FormFactor'], p['BIOSofUEFI'], p['DualofSingleBIOSUEFI'], p['Moederbordchipset'], p['Geheugentype'], p['MaximumGeheugengrootte'], p['HardeschijfBus'], p['CardInterface'], p['AantalPCIex16Slots'], p['LinkInterfaceATiCrossfireATiCrossfire'], p['VerbindingEthernet'], p['Netwerkchip'], p['BluetoothAanwezig'], p['VerbindingUSBFW'], p['VideoUit'], p['Verbinding'], p['AudioKanalen'], p['AudioUitgangen'], p['Audiochip'])
                else: pass



            elif componentTitle == 'Processorkoelers en Koelpasta':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Socket': p["Socket"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Heatpipes': p["Heatpipes"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Geluidsproductie': p["Geluidssterkte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Rotatiesnelheid minimaal': p["RotatiesnelheidMin"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Rotatiesnelheid maximaal': p["RotatiesnelheidMax"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Hoogte': p["Hoogte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Diameter ventilator': p["Diameter"] = value.text.strip()
                    product = productNode.nodeCPUFan('CPUFan', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Socket'], p['AansluitingProcessorkoeling'], p['Heatpipes'], p['Prestaties'], p['Geluidssterkte'], p['RotatiesnelheidMin'], p['RotatiesnelheidMax'], p['TypeKoeling'], p['Hoogte'], p['Diameter'], p['Kleuren'], p['Materialen'])
                else: pass


            elif componentTitle == 'Videokaarten':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Type GPU': p["Videochip"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Merk': p["Videochipfabrikant"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Turbo Frequency': p["MaximaleTurboFrequentie"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Videogeheugen': p["Geheugengrootte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Type geheugen': p["GeheugenType"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Kloksnelheid': p["GeheugenSnelheid"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Bandbreedte geheugenbus': p["GeheugenBusbreedte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Bus type': p["CardInterface"] = value.text.strip() # MAIN PROPERTY
                    elif spec.get_text(strip=True) == 'DirectX': p["DirectXVersie"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'OpenGL': p["OpenGLVersie"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Resolutie': p["MaximaleResolutie"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Resolutie': p["MaximaleResolutie"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Diepte': p["Lengte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Breedte': p["Breedte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Hoogte': p["Hoogte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Voedingsconnectoren': p["AantalSlots"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Minimaal benodigde voeding': p["Stroomverbruik"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Koelmethode': p["TypeKoeling"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Nvidia SLI': p["LinkInterface"] = value.text.strip()

                    product = productNode.nodeGraphicsCard('GraphicsCard', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Videochip'], p['ChipsetGeneratie'], p['Videochipfabrikant'], p['NominaleSnelheidVideochip'], p['MaximaleTurboFrequentie'], p['Rekenkernen'], p['Geheugengrootte'], p['GeheugenType'], p['GeheugenSnelheid'], p['GeheugenBusbreedte'], p['CardInterface'], p['VideoUit'], p['HoogsteHDMIVersie'], p['HoogsteDisplayPortVersie'], p['VideoAdapter'], p['DirectXVersie'], p['OpenGLVersie'], p['ShaderModel'], p['MaximaleResolutie'], p['Lengte'], p['Hoogte'], p['Breedte'], p['AantalSlots'], p['AantalPins'], p['Aantal6Pins'], p['Aantal8Pins'], p['Stroomverbruik'], p['TypeKoeling'], p['LinkInterface'])
                else: pass



            elif componentTitle == 'RAM-geheugen':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'RAM-geheugen': p["Geheugengrootte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Aantal geheugenkanalen': p["Aantal"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Geheugen': p["Geheugentype"] = value.text.strip() # MAIN PROPERTY
                    elif spec.get_text(strip=True) == 'Kloksnelheid geheugenmodule': p["GeheugenSpecificatie"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'CAS latency geheugenmodule': p["GeheugenCASLatency"] = value.text.strip()

                    product = productNode.nodeRAM('RAM', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Geheugengrootte'], p['Aantal'], p['Modulegrootte'], p['Geheugentype'], p['GeheugenSpecificatie'], p['LowVoltageDDR'], p['GeheugenCASLatency'])

                else: pass



            elif componentTitle == 'Computerbehuizingen':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Computerbehuizing': p["Behuizingtype"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Formaat moederbord': p["FormFactor"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Materiaal': p["Materialen"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Maximale lengte videokaart': p["GrafischeKaartMaximumLengte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Maximale hoogte processorkoeler': p["CPUKoelerMaximumHoogte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Kleur': p["Kleuren"] = value.text.strip()
                    elif spec.get_text(strip=True) == "3,5'' Bays (HDD)": p["BehuizingBayIntern"] = value.text.strip()
                    elif spec.get_text(strip=True) == "2,5'' Bays (HDD/SSD)": p["BehuizingBayExtern"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Locatie aansluiting voeding': p["VoedingPlaats"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Fan posities': p["FanPoorten"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Ventilator geleverd': p["MeegeleverdeFans"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Hoogte': p["Hoogte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Breedte': p["Breedte"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Diepte': p["Diepte"] = value.text.strip()
                    product = productNode.nodeCase('Case', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Behuizingtype'], p['FormFactor'], p['BehuizingPanel'], p['Materialen'], p['GrafischeKaartMaximumLengte'], p['CPUKoelerMaximumHoogte'], p['Kleuren'], p['BehuizingBayIntern'], p['BehuizingBayExtern'], p['AansluitingenVoorzijde'], p['VoedingPlaats'], p['VoedingFormFactor'], p['FanPoorten'], p['MeegeleverdeFans'], p['Kabelmanagement'], p['Hoogte'], p['Breedte'], p['Diepte'], p['Volume'], p['Gewicht'])
                else: pass



            elif componentTitle == 'Interne harde schijven (HDD)':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Opslagcapaciteit': p["Opslagcapaciteit"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Formaat harde schijf': p["BehuizingBayIntern"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Hardeschijfsnelheid': p["Schrijven"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Aansluiting': p["HardeschijfBusIntern"] = value.text.strip()


                    product = productNode.nodeStorage('Storage', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Opslagcapaciteit'], p['BehuizingBayIntern'], p['BehuizingBayIntern'], p['Hoogte'], p['Lezen'], p['Schrijven'], p['Rotatiesnelheid'], p['DriveCache'], p['CommandQueuing'], p['ReadSeekTime'], p['StroomverbruikLezen'], p['StroomverbruikSchrijven'])
                else: pass



            elif componentTitle == 'SSD (Solid State Drive)':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Opslagcapaciteit': p["Opslagcapaciteit"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Aansluiting': p["HardeschijfBusIntern"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Formaat harde schijf': p["BehuizingBayIntern"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Maximale leessnelheid': p["Lezen"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Maximale schrijfsnelheid': p["Schrijven"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Zoektijd (Seek time)': p["ReadSeekTime"] = value.text.strip()

                    product = productNode.nodeStorage('Storage', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Opslagcapaciteit'], p['HardeschijfBusIntern'], p['BehuizingBayIntern'], p['Hoogte'], p['Lezen'], p['Schrijven'], p['Rotatiesnelheid'], p['DriveCache'], p['CommandQueuing'], p['ReadSeekTime'], p['StroomverbruikLezen'], p['StroomverbruikSchrijven'])
                else: pass



            elif componentTitle == 'Barebones':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Garantie': p['Garantie'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Garantietype': p['Garantietype'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Processor': p['Processor'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Processornummer': p['Processornummer'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Processorkernen': p['Processorkernen'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Kloksnelheid': p['Kloksnelheid'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Processormerk': p['Processormerk'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Serie': p['Serie'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Geheugen': p['Geheugen'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'RAM-geheugen uitbreidbaar': p['RAM-geheugen uitbreidbaar'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Maximale hoeveelheid geheugen': p['Maximale hoeveelheid geheugen'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Geheugensloten totaal': p['Geheugensloten totaal'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Geheugenslot 1': p['Geheugenslot 1'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Geheugenslot 2': p['Geheugenslot 2'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Videokaart': p['Videokaart'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Videokaartfamilie': p['Videokaartfamilie'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Ethernetsnelheid': p['Ethernetsnelheid'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Wifi': p['Wifi'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Wifi-standaard': p['Wifi-standaard'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Bluetooth': p['Bluetooth'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'VGA-poort': p['VGA-poort'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'DVI': p['DVI'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'DisplayPort': p['DisplayPort'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'e-SATA': p['e-SATA'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'FireWire': p['FireWire'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'HDMI': p['HDMI'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'HDMI-poorten': p['HDMI-poorten'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'PS/2': p['PS/2'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Aantal usb-poorten': p['Aantal usb-poorten'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Usb-versie': p['Usb-versie'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Thunderbolt': p['Thunderbolt'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Hoofdtelefoonaansluiting': p['Hoofdtelefoonaansluiting'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Type HDMI-aansluiting': p['Type HDMI-aansluiting'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Vermogen': p['Vermogen'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Breedte': p['Breedte'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Kleur': p['Kleur'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Hoogte': p['Hoogte'] = value.text.strip()
                    product = productNode.nodeBarebones('Barebones', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Fabrikantcode'], p['Garantie'], p['Garantietype'], p['Processor'], p['Processornummer'], p['Processorkernen'], p['Kloksnelheid'], p['Processormerk'], p['Serie'], p['Geheugen'], p['RAM-geheugen uitbreidbaar'], p['Maximale hoeveelheid geheugen'], p['Geheugensloten totaal'], p['Geheugenslot 1'], p['Geheugenslot 2'], p['Videokaart'], p['Videokaartfamilie'], p['Ethernetsnelheid'], p['Wifi'], p['Wifi-standaard'], p['Bluetooth'], p['VGA-poort'], p['DVI'], p['DisplayPort'], p['e-SATA'], p['FireWire'], p['HDMI'], p['HDMI-poorten'], p['PS/2'], p['Aantal usb-poorten'], p['Usb-versie'], p['Thunderbolt'], p['Hoofdtelefoonaansluiting'], p['Type HDMI-aansluiting'], p['Vermogen'], p['Breedte'], p['Kleur'], p['Hoogte'])
                else: pass


            elif componentTitle == 'Voedingen (PSU)':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Fabrikantcode': p['Fabrikantcode'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Versie vormfactor': p['VersieVormfactor'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Vermogen': p['Vermogen'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Certificering': p['Certificering'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Gemiddelde levensduur': p['GemiddeldeLevensduur'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Breedte': p['Breedte'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Diepte': p['Diepte'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Hoogte': p['Hoogte'] = value.text.strip()
                    product = productNode.nodeVoeding('Voeding', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Fabrikantcode'], p['VersieVormfactor'], p['Vermogen'], p['Certificering'], p['GemiddeldeLevensduur'], p['Breedte'], p['Diepte'], p['Hoogte'])
                else: pass


            elif componentTitle == 'Geluidskaarten':

                if bool(PD['Fabrikantcode']):
                    p["ModelID"] = PD['Fabrikantcode']
                    p['Name'] = title
                    p['img'] = imgTag.get('src')

                    if spec.get_text(strip=True) == 'Merk': p["Merk"] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Fabrikantcode': p['Fabrikantcode'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Speaker kanalen': p['SpeakerKanalen'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Signaal-ruisverhouding': p['SignaalRuisverhouding'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Audio processor': p['AudioProcessor'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Optische ingang': p['OptischeIngang'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Breedte': p['Breedte'] = value.text.strip()
                    elif spec.get_text(strip=True) == 'Diepte': p['Diepte'] = value.text.strip()
                    product = productNode.nodeGeluidskaart('Soundcard', p['img'], p['ModelID'], p['Name'], p['Merk'], p['Fabrikantcode'], p['SpeakerKanalen'], p['SignaalRuisverhouding'], p['AudioProcessor'], p['OptischeIngang'], p['Breedte'], p['Diepte'])
                else: pass


        # CREATE RELATIONSHIP NODE OBJECT
        rel = relationNode.rel('Relationship', product, store, price, stock, href)
        db.create(rel)
        # print(db)


    else:
        print('ModelID a.k.a. Fabrikantcode ALREADY exists in Database')
        # print(db.cypher.execute_one('MATCH (n) WHERE n.ModelID = "{}" RETURN id(n), n'.format(PD['Fabrikantcode'])))




    # PRINT OUT COMPLETE Dictionary of THIS product
    # print(PD)
    print('Product Count: ', Statistic.productCount, PD)



    # Check Datetime at every loop
    now = datetime.now()

    if PD.get('Merk') is None: brand = "NULL"
    else: brand = PD['Merk']

    post = {'ModelID': PD['Fabrikantcode'], 'Name': title, 'Price': price, 'Brand': brand, 'Type': productType[componentTitle], 'Timestamp': int(time.mktime(now.timetuple()))}


    if productType[componentTitle] == 'CPU': mongodb.CPU.insert(post)
    elif productType[componentTitle] == 'Motherboard': mongodb.Motherboard.insert(post)
    elif productType[componentTitle] == 'CPUFan': mongodb.CPUFan.insert(post)
    elif productType[componentTitle] == 'GraphicsCard': mongodb.GraphicsCard.insert(post)
    elif productType[componentTitle] == 'RAM': mongodb.RAM.insert(post)
    elif productType[componentTitle] == 'Case': mongodb.Case.insert(post)
    elif productType[componentTitle] == 'PSU': mongodb.PSU.insert(post)
    elif productType[componentTitle] == 'Barebones': mongodb.Barebones.insert(post)
    elif productType[componentTitle] == 'Storage-HDD': mongodb.HDD.insert(post)
    elif productType[componentTitle] == 'Storage-SSD': mongodb.SSD.insert(post)
    else: mongodb.MISC.insert(post)










def interface(componentType):

    if componentType == 'Processoren': p = {'img': 'NULL', 'ModelID': 'NULL', 'Serie': 'NULL', 'Name': 'NULL', 'Merk': 'NULL', 'Socket': 'NULL', 'Garantie': 'NULL', 'Garantietype': 'NULL', "AantalCores": 'NULL', 'CPUSSpecNumber': 'NULL', 'Snelheid': 'NULL', 'MaximaleTurboFrequentie': 'NULL', 'GeheugenSpecificatie': 'NULL', 'BusSnelheid': 'NULL', 'Procestechnologie': 'NULL', 'ThermalDesignPower': 'NULL', 'GeïntegreerdeGraphics': 'NULL', 'Gpu': 'NULL', 'NominaleSnelheidVideochip': 'NULL', 'MaximaleSnelheidVideochip': 'NULL', 'CPUCacheLevel1': 'NULL', 'CPUCacheLevel2': 'NULL', 'CPUCacheLevel3': 'NULL', 'Threads': 'NULL', 'Virtualisatie': 'NULL', 'VirtualisatieType': 'NULL', 'CPUMultiplier': 'NULL', 'CPUstepping': 'NULL', 'CPUInstructieset': 'NULL', 'TypeKoeling': 'NULL'}
    elif componentType == 'Moederborden': p = {'img': 'NULL', 'ModelID': 'NULL', 'Merk': 'NULL', 'Socket': 'NULL', 'AantalSockets': 'NULL', 'FormFactor': 'NULL', 'BIOSofUEFI': 'NULL', 'DualofSingleBIOSUEFI': 'NULL', 'Moederbordchipset': 'NULL', 'Geheugentype': 'NULL', 'MaximumGeheugengrootte': 'NULL', 'HardeschijfBus': 'NULL', 'CardInterface': 'NULL', 'AantalPCIex16Slots': 'NULL', 'LinkInterfaceATiCrossfireATiCrossfire': 'NULL', 'VerbindingEthernet': 'NULL', 'Netwerkchip': 'NULL', 'BluetoothAanwezig': 'NULL', 'VerbindingUSBFW': 'NULL', 'VideoUit': 'NULL', 'Verbinding': 'NULL', 'AudioKanalen': 'NULL', 'AudioUitgangen': 'NULL', 'Audiochip': 'NULL'}
    elif componentType == 'Processorkoelers en Koelpasta': p = {'img': 'NULL', 'ModelID': 'NULL', 'Name': 'NULL', 'Merk': 'NULL', 'Socket': 'NULL', 'AansluitingProcessorkoeling': 'NULL', 'Heatpipes': 'NULL', 'Prestaties': 'NULL', 'Geluidssterkte': 'NULL', 'RotatiesnelheidMin': 'NULL', 'RotatiesnelheidMax': 'NULL', 'TypeKoeling': 'NULL', 'Hoogte': 'NULL', 'Diameter': 'NULL', 'Kleuren': 'NULL', 'Materialen': 'NULL'}
    elif componentType == 'Videokaarten': p = {'img': 'NULL', 'ModelID': 'NULL', 'Name': 'NULL', 'Merk': 'NULL', 'Videochip': 'NULL', 'ChipsetGeneratie': 'NULL', 'Videochipfabrikant': 'NULL', 'NominaleSnelheidVideochip': 'NULL', 'MaximaleTurboFrequentie': 'NULL', 'Rekenkernen': 'NULL', 'Geheugengrootte': 'NULL', 'GeheugenType': 'NULL', 'GeheugenSnelheid': 'NULL', 'GeheugenBusbreedte': 'NULL', 'CardInterface': 'NULL', 'VideoUit': 'NULL', 'HoogsteHDMIVersie': 'NULL', 'HoogsteDisplayPortVersie': 'NULL', 'VideoAdapter': 'NULL', 'DirectXVersie': 'NULL', 'OpenGLVersie': 'NULL', 'ShaderModel': 'NULL', 'MaximaleResolutie': 'NULL', 'Lengte': 'NULL', 'Hoogte': 'NULL', 'Breedte': 'NULL', 'AantalSlots': 'NULL', 'AantalPins': 'NULL', 'Aantal6Pins': 'NULL', 'Aantal8Pins': 'NULL', 'Stroomverbruik': 'NULL', 'TypeKoeling': 'NULL', 'LinkInterface': 'NULL'}
    elif componentType == 'Computerbehuizingen': p = {'img': 'NULL', 'ModelID': 'NULL', 'Merk': 'NULL', 'Behuizingtype': 'NULL', 'FormFactor': 'NULL', 'BehuizingPanel': 'NULL', 'Materialen': 'NULL', 'GrafischeKaartMaximumLengte': 'NULL', 'CPUKoelerMaximumHoogte': 'NULL', 'Kleuren': 'NULL', 'BehuizingBayIntern': 'NULL', 'BehuizingBayExtern': 'NULL', 'AansluitingenVoorzijde': 'NULL', 'VoedingPlaats': 'NULL', 'VoedingFormFactor': 'NULL', 'FanPoorten': 'NULL', 'MeegeleverdeFans': 'NULL', 'Kabelmanagement': 'NULL', 'Hoogte': 'NULL', 'Breedte': 'NULL', 'Diepte': 'NULL', 'Volume': 'NULL', 'Gewicht': 'NULL'}
    elif componentType == 'RAM-geheugen': p = {'img': 'NULL', 'ModelID': 'NULL', 'Name': 'NULL', 'Merk': 'NULL', 'Geheugengrootte': 'NULL', 'Aantal': 'NULL', 'Modulegrootte': 'NULL', 'Geheugentype': 'NULL', 'GeheugenSpecificatie': 'NULL', 'LowVoltageDDR': 'NULL', 'GeheugenCASLatency': 'NULL'}
    elif componentType == 'Interne harde schijven (HDD)': p = {'img': 'NULL', 'ModelID': 'NULL', 'Name': 'NULL', 'Merk': 'NULL', 'Opslagcapaciteit': 'NULL', 'HardeschijfBusIntern': 'NULL', 'BehuizingBayIntern': 'NULL', 'Hoogte': 'NULL', 'Lezen': 'NULL', 'Schrijven': 'NULL', 'Rotatiesnelheid': 'NULL', 'DriveCache': 'NULL', 'CommandQueuing': 'NULL', 'ReadSeekTime': 'NULL', 'StroomverbruikLezen': 'NULL', 'StroomverbruikSchrijven': 'NULL'}
    elif componentType == 'SSD (Solid State Drive)': p = {'img': 'NULL', 'ModelID': 'NULL', 'Name': 'NULL', 'Merk': 'NULL', 'Opslagcapaciteit': 'NULL', 'HardeschijfBusIntern': 'NULL', 'BehuizingBayIntern': 'NULL', 'Hoogte': 'NULL', 'Lezen': 'NULL', 'Schrijven': 'NULL', 'Rotatiesnelheid': 'NULL', 'DriveCache': 'NULL', 'CommandQueuing': 'NULL', 'ReadSeekTime': 'NULL', 'StroomverbruikLezen': 'NULL', 'StroomverbruikSchrijven': 'NULL'}
    elif componentType == 'Barebones': p = {'img': 'NULL', 'ModelID': 'NULL', 'Name': 'NULL', 'Gewicht': 'NULL', 'Thunderbolt': 'NULL', 'HDMI': 'NULL', 'Garantietype': 'NULL', 'Fabrikantcode': 'NULL', 'Geheugenslot 2': 'NULL', 'e-SATA': 'NULL', 'DisplayPort': 'NULL', 'Type HDMI-aansluiting': 'NULL', 'PS/2': 'NULL', 'DVI': 'NULL', 'Vermogen': 'NULL', 'Artikelnummer': 'NULL', 'Aantal DVI-uitgangen': 'NULL', 'Aantal usb-poorten': 'NULL', 'Hoofdtelefoonaansluiting': 'NULL', 'Ethernetsnelheid': 'NULL', 'Kleur': 'NULL', 'HDMI-poorten': 'NULL', 'Type DVI-aansluiting': 'NULL', 'Breedte': 'NULL', 'Geheugen': 'NULL', 'Wifi': 'NULL', 'Merk': 'NULL', 'Garantie': 'NULL', 'FireWire': 'NULL', 'Hoogte': 'NULL', 'Geheugensloten totaal': 'NULL', 'Geheugenslot 1': 'NULL', 'VGA-poort': 'NULL', 'Usb-versie': 'NULL', 'RAM-geheugen uitbreidbaar': 'NULL', 'Maximale hoeveelheid geheugen': 'NULL'}
    elif componentType == 'Voedingen (PSU)': p = {'img': 'NULL', 'ModelID': 'NULL', 'Name': 'NULL', 'Merk': 'NULL', 'Fabrikantcode': 'NULL', 'VersieVormfactor': 'NULL', 'Vermogen': 'NULL', 'Certificering': 'NULL', 'GemiddeldeLevensduur': 'NULL', 'Breedte': 'NULL', 'Diepte': 'NULL', 'Hoogte': 'NULL'}
    elif componentType == 'Geluidskaarten': p = {'img': 'NULL', 'ModelID': 'NULL', 'Name': 'NULL', 'Merk': 'NULL', 'Fabrikantcode': 'NULL', 'SpeakerKanalen': 'NULL', 'SignaalRuisverhouding': 'NULL', 'AudioProcessor': 'NULL', 'OptischeIngang': 'NULL', 'Breedte': 'NULL', 'Diepte': 'NULL'}
    return p





class timeConvert():

    def convert(self, timestamp):
        self.timestamp = timestamp

        return datetime.datetime.fromtimestamp(int(self.timestamp)).strftime('%Y-%m-%d %H:%M:%S')



class relationNode():

    def rel(self, product, store, productPrice, productStock, productUrl):
        n = Relationship(product, 'SOLD_AT', store, Price=productPrice, InStock=str(productStock), productUrl=productUrl)
        return n



class storeObject():

    def createStore(self, name, storeName, storeAddress, storePostal, storeCity, storeUrl, storePhone):
        n = Node(name, Name=storeUrl, Store=storeName, Address=storeAddress, Postalcode=storePostal, City=storeCity, Website=storeUrl, Phone=storePhone)
        return n



class productNode():

    def nodeCPU(self, img, Socket, ModelID, Serie, Name, Merk, Garantie, Garantietype, AantalCores, CPUSSpecNumber, Snelheid, MaximaleTurboFrequentie, GeheugenSpecificatie, BusSnelheid, Procestechnologie, ThermalDesignPower, GeïntegreerdeGraphics, Gpu, NominaleSnelheidVideochip, MaximaleSnelheidVideochip, CPUCacheLevel1, CPUCacheLevel2, CPUCacheLevel3, Threads, Virtualisatie, VirtualisatieType, CPUMultiplier, CPUstepping, CPUInstructieset, TypeKoeling):
        n = Node('Component', 'CPU', img=img, Socket=Socket, ModelID=ModelID, Serie=Serie, Name=Name, Merk=Merk, Garantie=Garantie, Garantietype=Garantietype, AantalCores=AantalCores, CPUSSpecNumber=CPUSSpecNumber, Snelheid=Snelheid, MaximaleTurboFrequentie=MaximaleTurboFrequentie, GeheugenSpecificatie=GeheugenSpecificatie, BusSnelheid=BusSnelheid, Procestechnologie=Procestechnologie, ThermalDesignPower=ThermalDesignPower, GeïntegreerdeGraphics=GeïntegreerdeGraphics, Gpu=Gpu, NominaleSnelheidVideochip=NominaleSnelheidVideochip, MaximaleSnelheidVideochip=MaximaleSnelheidVideochip, CPUCacheLevel1=CPUCacheLevel1, CPUCacheLevel2=CPUCacheLevel2, CPUCacheLevel3=CPUCacheLevel3, Threads=Threads, Virtualisatie=Virtualisatie, VirtualisatieType=VirtualisatieType, CPUMultiplier=CPUMultiplier, CPUstepping=CPUstepping, CPUInstructieset=CPUInstructieset, TypeKoeling=TypeKoeling)
        return n

    def nodeMotherboard(self, img, ModelID, Name, Merk, Socket, AantalSockets, FormFactor, BIOSofUEFI, DualofSingleBIOSUEFI, Moederbordchipset, Geheugentype, MaximumGeheugengrootte, HardeschijfBus, CardInterface, AantalPCIex16Slots, LinkInterfaceATiCrossfireATiCrossfire, VerbindingEthernet,Netwerkchip,BluetoothAanwezig,VerbindingUSBFW,VideoUit,Verbinding,AudioKanalen,AudioUitgangen,Audiochip):
        n = Node('Component', 'Motherboard', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Socket=Socket, AantalSockets=AantalSockets, FormFactor=FormFactor, BIOSofUEFI=BIOSofUEFI, DualofSingleBIOSUEFI=DualofSingleBIOSUEFI, Moederbordchipset=Moederbordchipset, Geheugentype=Geheugentype, MaximumGeheugengrootte=MaximumGeheugengrootte, HardeschijfBus=HardeschijfBus, CardInterface=CardInterface, AantalPCIex16Slots=AantalPCIex16Slots, LinkInterfaceATiCrossfireATiCrossfire=LinkInterfaceATiCrossfireATiCrossfire, VerbindingEthernet=VerbindingEthernet, Netwerkchip=Netwerkchip, BluetoothAanwezig=BluetoothAanwezig, VerbindingUSBFW=VerbindingUSBFW, VideoUit=VideoUit, Verbinding=Verbinding, AudioKanalen=AudioKanalen, AudioUitgangen=AudioUitgangen, Audiochip=Audiochip)
        return n

    def nodeCPUFan(self, img, ModelID, Name, Merk, Socket, AansluitingProcessorkoeling, Heatpipes, Prestaties, Geluidssterkte, RotatiesnelheidMin, RotatiesnelheidMax, TypeKoeling, Hoogte, Diameter, Kleuren, Materialen):
        n = Node('Component', 'CPUFan', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Socket=Socket, AansluitingProcessorkoeling=AansluitingProcessorkoeling, Heatpipes=Heatpipes, Prestaties=Prestaties, Geluidssterkte=Geluidssterkte, RotatiesnelheidMin=RotatiesnelheidMin, RotatiesnelheidMax=RotatiesnelheidMax, TypeKoeling=TypeKoeling, Hoogte=Hoogte, Diameter=Diameter, Kleuren=Kleuren, Materialen=Materialen)
        return n

    def nodeGraphicsCard(self, img, ModelID, Name, Merk, Videochip, ChipsetGeneratie, Videochipfabrikant, NominaleSnelheidVideochip, MaximaleTurboFrequentie, Rekenkernen, Geheugengrootte, GeheugenType, GeheugenSnelheid, GeheugenBusbreedte, CardInterface, VideoUit, HoogsteHDMIVersie, HoogsteDisplayPortVersie, VideoAdapter, DirectXVersie, OpenGLVersie, ShaderModel, MaximaleResolutie, Lengte, Hoogte, Breedte, AantalSlots, AantalPins, Aantal6Pins, Aantal8Pins, Stroomverbruik, TypeKoeling, LinkInterface):
        n = Node('Component', 'GraphicsCard', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Videochip=Videochip, ChipsetGeneratie=ChipsetGeneratie, Videochipfabrikant=Videochipfabrikant, NominaleSnelheidVideochip=NominaleSnelheidVideochip, MaximaleTurboFrequentie=MaximaleTurboFrequentie, Rekenkernen=Rekenkernen, Geheugengrootte=Geheugengrootte, GeheugenType=GeheugenType, GeheugenSnelheid=GeheugenSnelheid, GeheugenBusbreedte=GeheugenBusbreedte, CardInterface=CardInterface, VideoUit=VideoUit, HoogsteHDMIVersie=HoogsteHDMIVersie, HoogsteDisplayPortVersie=HoogsteDisplayPortVersie, VideoAdapter=VideoAdapter, DirectXVersie=DirectXVersie, OpenGLVersie=OpenGLVersie, ShaderModel=ShaderModel, MaximaleResolutie=MaximaleResolutie, Lengte=Lengte, Hoogte=Hoogte, Breedte=Breedte, AantalSlots=AantalSlots, AantalPins=AantalPins, Aantal6Pins=Aantal6Pins, Aantal8Pins=Aantal8Pins, Stroomverbruik=Stroomverbruik, TypeKoeling=TypeKoeling, LinkInterface=LinkInterface)
        return n

    def nodeRAM(self, img, ModelID, Name, Merk, Geheugengrootte, Aantal, Modulegrootte, Geheugentype, GeheugenSpecificatie, LowVoltageDDR, GeheugenCASLatency):
        n = Node('Component', 'RAM', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Geheugengrootte=Geheugengrootte, Aantal=Aantal, Modulegrootte=Modulegrootte, Geheugentype=Geheugentype, GeheugenSpecificatie=GeheugenSpecificatie, LowVoltageDDR=LowVoltageDDR, GeheugenCASLatency=GeheugenCASLatency)
        return n

    def nodeCase(self, img, ModelID, Name, Merk, Behuizingtype, FormFactor, BehuizingPanel, Materialen, GrafischeKaartMaximumLengte, CPUKoelerMaximumHoogte, Kleuren, BehuizingBayIntern, BehuizingBayExtern, AansluitingenVoorzijde, VoedingPlaats, VoedingFormFactor, FanPoorten, MeegeleverdeFans, Kabelmanagement, Hoogte, Breedte, Diepte, Volume, Gewicht):
        n = Node('Component', 'Case', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Behuizingtype=Behuizingtype, FormFactor=FormFactor, BehuizingPanel=BehuizingPanel, Materialen=Materialen, GrafischeKaartMaximumLengte=GrafischeKaartMaximumLengte, CPUKoelerMaximumHoogte=CPUKoelerMaximumHoogte, Kleuren=Kleuren, BehuizingBayIntern=BehuizingBayIntern, BehuizingBayExtern=BehuizingBayExtern, AansluitingenVoorzijde=AansluitingenVoorzijde, VoedingPlaats=VoedingPlaats, VoedingFormFactor=VoedingFormFactor, FanPoorten=FanPoorten, MeegeleverdeFans=MeegeleverdeFans, Kabelmanagement=Kabelmanagement, Hoogte=Hoogte, Breedte=Breedte, Diepte=Diepte, Volume=Volume, Gewicht=Gewicht)
        return n

    def nodeStorage(self, img, ModelID, Name, Merk, Opslagcapaciteit, HardeschijfBusIntern, BehuizingBayIntern, Hoogte, Lezen, Schrijven, Rotatiesnelheid, DriveCache, CommandQueuing, ReadSeekTime, StroomverbruikLezen, StroomverbruikSchrijven):
        n = Node('Component', 'Storage', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Opslagcapaciteit=Opslagcapaciteit, HardeschijfBusIntern=HardeschijfBusIntern, BehuizingBayIntern=BehuizingBayIntern, Hoogte=Hoogte, Lezen=Lezen, Schrijven=Schrijven, Rotatiesnelheid=Rotatiesnelheid, DriveCache=DriveCache, CommandQueuing=CommandQueuing, ReadSeekTime=ReadSeekTime, StroomverbruikLezen=StroomverbruikLezen, StroomverbruikSchrijven=StroomverbruikSchrijven)
        return n

    def nodeBarebones(self, img, ModelID, Name, Merk, Fabrikantcode, Garantie, Garantietype, Processor, Processornummer, Processorkernen, Kloksnelheid, Processormerk, Serie, Geheugen, RAMgeheugenUitbreidbaar, MaximaleHoeveelheidGeheugen, GeheugenslotenTotaal, Geheugenslot1, Geheugenslot2, Videokaart, Videokaartfamilie, Ethernetsnelheid, Wifi, WifiStandaard, Bluetooth, VGAPoort, DVI, DisplayPort, eSATA, FireWire, HDMI, HDMIpoorten, PS2, AantalUsbPoorten, UsbVersie, Thunderbolt, Hoofdtelefoonaansluiting, TypeHDMIaansluiting, Vermogen, Breedte, Kleur, Hoogte):
        n = Node('Component', 'Barebones', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Fabrikantcode=Fabrikantcode, Garantie=Garantie, Garantietype=Garantietype, Processor=Processor, Processornummer=Processornummer, Processorkernen=Processorkernen, Kloksnelheid=Kloksnelheid, Processormerk=Processormerk, Serie=Serie, Geheugen=Geheugen, RAMgeheugenUitbreidbaar=RAMgeheugenUitbreidbaar, MaximaleHoeveelheidGeheugen=MaximaleHoeveelheidGeheugen, GeheugenslotenTotaal=GeheugenslotenTotaal, Geheugenslot1=Geheugenslot1, Geheugenslot2=Geheugenslot2, Videokaart=Videokaart, Videokaartfamilie=Videokaartfamilie, Ethernetsnelheid=Ethernetsnelheid, Wifi=Wifi, WifiStandaard=WifiStandaard, Bluetooth=Bluetooth, VGAPoort=VGAPoort, DVI=DVI, DisplayPort=DisplayPort, eSATA=eSATA, FireWire=FireWire, HDMI=HDMI, HDMIpoorten=HDMIpoorten, PS2=PS2, AantalUsbPoorten=AantalUsbPoorten, UsbVersie=UsbVersie, Thunderbolt=Thunderbolt, Hoofdtelefoonaansluiting=Hoofdtelefoonaansluiting, TypeHDMIaansluiting=TypeHDMIaansluiting, Vermogen=Vermogen, Breedte=Breedte, Kleur=Kleur, Hoogte=Hoogte)
        return n

    def nodeVoeding(self, img, ModelID, Name, Merk, Fabrikantcode, VersieVormfactor, Vermogen, Certificering, GemiddeldeLevensduur, Breedte, Diepte, Hoogte):
        n = Node('Component', 'Voeding', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Fabrikantcode=Fabrikantcode, VersieVormfactor=VersieVormfactor, Vermogen=Vermogen, Certificering=Certificering, GemiddeldeLevensduur=GemiddeldeLevensduur, Breedte=Breedte, Diepte=Diepte, Hoogte=Hoogte)
        return n

    def nodeGeluidskaart(self, img, ModelID, Name, Merk, Fabrikantcode, SpeakerKanalen, SignaalRuisverhouding, AudioProcessor, OptischeIngang, Breedte, Diepte):
        n = Node('Component', 'Geluidskaarts', img=img, ModelID=ModelID, Name=Name, Merk=Merk, Fabrikantcode=Fabrikantcode, SpeakerKanalen=SpeakerKanalen, SignaalRuisverhouding=SignaalRuisverhouding, AudioProcessor=AudioProcessor, OptischeIngang=OptischeIngang, Breedte=Breedte, Diepte=Diepte)
        return n




<<<<<<< HEAD
class Database:

    def local(self):
        db = Graph("http://localhost:7474/db/data/")
        return db

    def online(self):
        db = Graph("http://localhost:7484/db/data/")
        return db
=======
'''
<<<<<<< Updated upstream
def htmlOld(sourceCode):
    # wanneer gaat om Tables
    print(sourceCode)
    print("*******************************")
    # TODO: Check alle tabellen <DL>
    #for tech in sourceCode.product-specs--item-title #product-specs--item-spec
=======
>>>>>>> Stashed changes
'''
>>>>>>> FETCH_HEAD




if __name__ == '__main__':
    main()