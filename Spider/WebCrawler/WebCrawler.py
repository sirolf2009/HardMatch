#WebCrawler Prototype
#Rene van der Horst

#Dit programma pakt data van de site http://www.alternate.nl

import requests
from bs4 import BeautifulSoup

alternate_url = 'https://www.alternate.nl/html/highlights/page.html?hgid=286&tgid=963&tk=7&lk=9463'
alternate_source_code = requests.get(alternate_url)

plain_text = alternate_source_code.text

soup = BeautifulSoup(plain_text)
for link in soup.findAll('a',{'class':'h1x1'}):
    href = link.get('href')
    print(href)

