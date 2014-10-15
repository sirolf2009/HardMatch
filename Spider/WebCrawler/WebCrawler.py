#WebCrawler Prototype

__author__ = "Rene van der Horst, Basit Hussain"
__copyright__ = "Copyright 2007, The Cogent Project"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

#Indentation: 4 spaces
#Variable naming: skeleton case

#This program picks up data from alternate.nl

# 1. 2 websites
# 2. Strings parsen
# 3. py2neo importeren

import requests
from bs4 import BeautifulSoup

#alternate.nl
alternate_url = 'https://www.alternate.nl/html/highlights/page.html?hgid=286&tgid=963&tk=7&lk=9463'
alternate_source_code = requests.get(alternate_url)

alternate_plain_text = alternate_source_code.text
alternate_soup = BeautifulSoup(alternate_plain_text)

for processor in alternate_soup.findAll('a', {'class': 'h1x1'}):
    processor_manufacturer = processor.find_next('span', {'class': 'manufacturerName'})
    processor_name = processor.find_next('span', {'class': 'name'})
    processor_price = processor.find_next('span', {'class': 'price'})

    print(processor_manufacturer.text)
    print(processor_name.text)
    print(processor_price.text)
    print("")

#mediamarkt.nl
mediamarkt_graphicscards_url = 'http://www.mediamarkt.nl/mcs/productlist/Videokaarten,10259,482720.html?langId=-11'
mediamarkt_graphicscards_source_code = requests.get(mediamarkt_graphicscards_url)

mediamarkt_graphicscards_plain_text = mediamarkt_graphicscards_source_code.text
mediamarkt_soup = BeautifulSoup(mediamarkt_graphicscards_plain_text)

for link2 in mediamarkt_soup.findAll('div', {'class': 'product-wrapper'}):
    href2 = link2.get('href')
    href2 = str(href2)
    print('href2:' + href2)

