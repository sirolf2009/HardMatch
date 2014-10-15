__author__ = 'Cassandra'
import requests
from bs4 import BeautifulSoup

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
                     href = 'http://www.mediamarkt.nl'+tekst.get('href')
                     detailSpider(href)
                elif substring2 in title:
                    href = 'http://www.mediamarkt.nl'+tekst.get('href')
                    detailSpider(href)

'''
Crawl een product detail pagina op basis van een link en return een videokaart object
'''
def detailSpider(detailadress):
    source_code = requests.get(detailadress)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    prijs_string = ''
    first_digit = soup.find('span',{'class','p-3'})

    naam_raw = soup.find('h1',{'itemprop':'name'})
    artnmr_raw = soup.find('dd',{'itemprop':'sku'})
    naam_clean = naam_raw.string
    artnmr_clean = artnmr_raw.string
    v = Videokaart()
    Videokaart.setnaam(v,naam_clean)
    Videokaart.setartnnmr(v,artnmr_clean)
    Videokaart.displayvideokaart(v)



class Videokaart():
    naam = ''
    artikelnummer = ''

    def displayvideokaart(self):
        print('Productnaam: '+self.naam)
        print('Artikelnummer: '+self.artikelnummer)

    def setnaam(self,naam):
        self.naam = naam

    def setartnnmr(self,artnmr):
        self.artikelnummer = artnmr

mediaMarkt_spider()