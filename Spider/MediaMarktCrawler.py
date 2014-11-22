

__author__ = 'Cassandra'
from py2neo import neo4j,node,rel

import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, node, rel

graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")


graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

# Zoek naar links van detailpagina's en geef deze door aan de factory
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

<<<<<<< HEAD
def getCategories():
    s1 = 'Werkgeheugen'
    s2 = 'Behuizingen'
    s3 = 'Moederbord'
    s4 = 'Processor'
    s5 = 'Video'
    s6 = 'Geluidskaart'
    s7 = 'Koeling'
    s8 = 'Geheugenmodules'
    s9 = 'Harddisks'
    s10 = 'CD'
    categories = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    return categories

def topLevelSpider(url,categories)
    source_code = requests.get(url)
=======

# Experimenteel,probeer de prijs te parsen
def prijs_parser(detailadress):
    source_code = requests.get(detailadress)
>>>>>>> origin/master
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for li in soup.findAll('li', {'class': 'active child-active'}):
        content = li.find('a').contents[0]
        for i in range(len(categories)):
            if categories[i].getName() in content:
                link = 'http://www.informatique.nl' + (td.find('a')['href'])
                midLevelSpider(link, categories[i].getSubs())


def videoKaartFactory(detailadress):
    source_code = requests.get(detailadress)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    v = VideoKaart()

    for omschrijving in soup.findAll('dt'):
<<<<<<< HEAD
=======
        check = omschrijving.string
        if check is not None:
            if 'Grafiek' in check:
                gr_freq = omschrijving.findNextSibling('dd')
                gr_freq = gr_freq.string
                Videokaart.setgr_freq(v, gr_freq)
            elif 'Fabrikant' in check:
                f_chipset = omschrijving.findNextSibling('dd')
                f_chipset = f_chipset.string
                Videokaart.setf_chipset(v, f_chipset)
            elif 'chipset' in check:
                g_chipset = omschrijving.findNextSibling('dd')
                g_chipset = g_chipset.string
                Videokaart.setg_chipset(v, g_chipset)
            elif 'model' in check:
                s_model = omschrijving.findNextSibling('dd')
                s_model = s_model.string
                Videokaart.sets_model(v, s_model)
            elif 'grootte' in check:
                geheugen = omschrijving.findNextSibling('dd')
                geheugen = geheugen.string
                Videokaart.setgeheugen(v, geheugen)
            elif 'Geheugen-klokfrequentie' in check:
                ge_freq = omschrijving.findNextSibling('dd')
                ge_freq = ge_freq.string
                Videokaart.setge_freq(v, ge_freq)
            elif 'Type' in check:
                gr_geheugen = omschrijving.findNextSibling('dd')
                gr_geheugen = gr_geheugen.string
                Videokaart.setgr_geheugen(v, gr_geheugen)
            elif 'interface' in check:
                ge_interface = omschrijving.findNextSibling('dd')
                ge_interface = ge_interface.string
                Videokaart.setge_interface(v, ge_interface)
            elif 'API' in check:
                api = omschrijving.findNextSibling('dd')
                api = api.string
                Videokaart.setapi(v, api)
            elif 'Aansluitingen' in check:
                aansluitingen = omschrijving.findNextSibling('dd')
                aansluitingen = aansluitingen.string
                Videokaart.setaansluitingen(v, aansluitingen)
        else:
            print(omschrijving)

    Videokaart.setnaam(v, naam_clean)
    Videokaart.setartnnmr(v, artnmr_clean)
    Videokaart.displayvideokaart(v)


def videoKaartFactory(detailadress):
    source_code = requests.get(detailadress)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    v = VideoKaart()

    for omschrijving in soup.findAll('dt'):
>>>>>>> origin/master
        key = omschrijving.string
        if key is not None:
            raw_value = omschrijving.findNextSibling('dd')
            value = raw_value.string
            VideoKaart.addGegeven(v, key, value)
<<<<<<< HEAD
=======

    naam_raw = soup.find('h1', {'itemprop': 'name'})
    artnmr_raw = soup.find('dd', {'itemprop': 'sku'})
    naam_clean = naam_raw.string
    artnmr_clean = artnmr_raw.string
    VideoKaart.addGegeven(v, 'Naam', naam_clean)
    VideoKaart.addGegeven(v, 'Artikelnummer', artnmr_clean)
    VideoKaart.printGegevens(v)


class Videokaart():
    naam = ''
    artikelnummer = ''
    gr_freq = ''
    f_chipset = ''
    g_chipset = ''
    s_model = ''
    geheugen = ''
    ge_freq = ''
    gr_geheugen = ''
    ge_interface = ''
    api = ''
    aansluitingen = ''
>>>>>>> origin/master

    naam_raw = soup.find('h1', {'itemprop': 'name'})
    naam_clean = naam_raw.string
    prijs_raw = soup.find('div', {'class':'price big'})
    prijs = prijs_raw.string
    VideoKaart.addGegeven(v, 'Naam', naam_clean)
    VideoKaart.addGegeven(v,'Prijs',prijs)
    VideoKaart.printGegevens(v)


class VideoKaart():
    gegevens = {}

    def addGegeven(self, key, value):
        self.gegevens[key] = value

    def printGegevens(self):
        for x in self.gegevens:
            print(x)
            print(self.gegevens[x])

<<<<<<< HEAD
videoKaartFactory('http://www.mediamarkt.nl/mcs/product/CORSAIR-Mac-Memory-16GB-geheugenmodules,10259,482712,927805.html?langId=-11&et_cid=66&et_lid=235&et_sub=1-CORSAIR%20Mac%20Memory%2016GB%20geheugenmodules')
=======
class VideoKaart():
    gegevens = {}

    def addGegeven(self, key, value):
        self.gegevens[key] = value

    def printGegevens(self):
        for x in self.gegevens:
            print(x)
            print(self.gegevens[x])

   # def saveVideoKaart(self):



mediaMarkt_spider()
>>>>>>> origin/master
