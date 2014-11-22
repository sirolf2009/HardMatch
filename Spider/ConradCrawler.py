__author__ = 'Basit'
import requests
from bs4 import BeautifulSoup

def branderFinder():
    url = 'https://www.conrad.nl/nl/computer-kantoor/pc-componenten.html'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    substring1 = 'brander'
    for tekst in soup.findAll('a'):
        title = tekst.string
        if title is not None:
            if substring1 in title:
                href = 'http://www.conrad.nl' + tekst.get('href')
                branderFinder(href)

def branderFinder(link):
    source_code = requests.get(link)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    substring1 = 'brander'
    substring2 = 'specificatie'
    for tekst in soup.findAll('h2'):
        tabel_naam = tekst.string
        if tabel_naam is not None:
            if substring2 in tabel_naam:
                componentFactory(link)
    for tekst in soup.findAll('a'):
        title = tekst.string
        if title is not None:
            if substring1 in title:
                href = 'http://www.conrad.nl' + tekst.get('href')
                branderFinder(href)

def experimental(link):
    source_code = requests.get(link)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    substring1 = 'brander'
    for tekst in soup.findAll('a'):
        print(tekst)
        '''title = tekst.string
        if title is not None:
            if substring1 in title:
                print('yes')
                print(tekst.get('href'))
                print(tekst)'''


def componentFactory(detailadress):
    source_code = requests.get(detailadress)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    c = Component()
    naam_raw = soup.find('h1', {'class': 'c-productdetails-title'})
    prijs_raw = soup.find('div', {'class': 'product-price'})
    naam_clean = naam_raw.string
    prijs_clean = prijs_raw.string
    Component.addGegeven(c, 'Naam', naam_clean)
    Component.addGegeven(c, 'Prijs', prijs_clean)

    for omschrijving in soup.findAll('td',{'class':'column-left'}):
        key = omschrijving.string
        if key is not None:
            raw_value = omschrijving.findNextSibling('td')
            value = raw_value.string
            Component.addGegeven(c, key, value)

    Component.printGegevens(c)

class Component():
    gegevens = {}

    def addGegeven(self, key, value):
        self.gegevens[key] = value

    def printGegevens(self):
        for x in self.gegevens:
            print(x)
            print(self.gegevens[x])

#componentFactory('https://www.conrad.nl/nl/buffalo-brxl-pc6u2b-eu-externe-blu-ray-brander-retail-usb-20-zwart-417529.html')
#branderFinder('https://www.conrad.nl/nl/computer-kantoor/pc-componenten/drives-branders/externe-blu-ray-branders.html')
experimental('https://www.conrad.nl/nl/computer-kantoor/pc-componenten/drives-branders/externe-blu-ray-branders.html')