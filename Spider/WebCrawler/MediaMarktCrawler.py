__author__ = 'Cassandra'
import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, node, rel

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


# Experimenteel,probeer de prijs te parsen
def prijs_parser(detailadress):
    source_code = requests.get(detailadress)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    prijs_string = ''
    first_digit = soup.find('span', {'class': 'p-5'})
    '''test = first_digit.text'''
    print(first_digit)


#Crawl een product detail pagina op basis van een link en return een videokaart object
def videokaartFactory(detailadress):
    source_code = requests.get(detailadress)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    naam_raw = soup.find('h1', {'itemprop': 'name'})
    artnmr_raw = soup.find('dd', {'itemprop': 'sku'})
    naam_clean = naam_raw.string
    artnmr_clean = artnmr_raw.string
    v = Videokaart()

    for omschrijving in soup.findAll('dt'):
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
        key = omschrijving.string
        if key is not None:
            raw_value = omschrijving.findNextSibling('dd')
            value = raw_value.string
            VideoKaart.addGegeven(v, key, value)

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

    def displayvideokaart(self):
        to_print = "Productnaam: {0}\nArtikelnummer: {1}\nGrafiek-klokfrequentie: {2}\nFabrikant grafische chipset: {3}\n" \
                   "Grafische chipset: {4}\nShader model: {5}\nGeheugengrootte: {6}\nGeheugen-klokfrequentie: {7}\n" \
                   "Type grafisch geheugen: {8}\nGeheugeninterface: {9}\nAPI-ondersteuning: {10}\n" \
                   "Aansluitingen: {11}".format(self.naam, self.artikelnummer, self.gr_freq, self.f_chipset,
                                                self.g_chipset,
                                                self.s_model, self.geheugen, self.ge_freq, self.gr_geheugen,
                                                self.ge_interface,
                                                self.api, self.aansluitingen)
        print(to_print)

    def setnaam(self, naam):
        self.naam = naam

    def setartnnmr(self, artnmr):
        self.artikelnummer = artnmr

    def setgr_freq(self, gr_freq):
        self.gr_freq = gr_freq

    def setf_chipset(self, f_chipset):
        self.f_chipset = f_chipset

    def setg_chipset(self, g_chipset):
        self.g_chipset = g_chipset

    def sets_model(self, s_model):
        self.s_model = s_model

    def setgeheugen(self, geheugen):
        self.geheugen = geheugen

    def setge_freq(self, ge_freq):
        self.ge_freq = ge_freq

    def setgr_geheugen(self, gr_geheugen):
        self.gr_geheugen = gr_geheugen

    def setge_interface(self, ge_interface):
        self.ge_interface = ge_interface

    def setapi(self, api):
        self.api = api

    def setaansluitingen(self, aansluitingen):
        self.aansluitingen = aansluitingen


class VideoKaart():
    gegevens = {}

    def addGegeven(self, key, value):
        self.gegevens[key] = value

    def printGegevens(self):
        for x in self.gegevens:
            print(x)
            print(self.gegevens[x])

    def saveVideoKaart(self):



mediaMarkt_spider()