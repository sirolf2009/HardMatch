#WebCrawler Prototype

__author__ = "Rene van der Horst, Basit Hussain"
__copyright__ = "Copyright 2014, HardMatch Project"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

#Indentation: 4 spaces
#Variable naming: skeleton case

#This program picks up data from alternate.nl

# 1. 2 websites
# 3. py2neo importeren

import requests
from bs4 import BeautifulSoup

#alternate.nl
alternate_url = 'https://www.alternate.nl/html/highlights/page.html?hgid=286&tgid=963&tk=7&lk=9463'
alternate_source_code = requests.get(alternate_url)

alternate_plain_text = alternate_source_code.text
alternate_soup = BeautifulSoup(alternate_plain_text)


def get_processor_links():
    link_list = []
    for processor in alternate_soup.findAll('a', {'class': 'h1x1'}):
        link = processor.get('href')
        full_link = 'https://www.alternate.nl' + link
        link_list.append(full_link)
    return link_list


def get_processor_data(link_list):
    number = 0
    for link_url in link_list:
        url_source_code = requests.get(link_url)
        url_plain_text = url_source_code.text
        url_soup = BeautifulSoup(url_plain_text)

        processor_brand = url_soup.find_all('span', {'itemprop': 'brand'})
        processor_name = url_soup.find_all('meta', {'itemprop': 'name'})
        processor_price = url_soup.find_all('span', {'itemprop': 'price'})
        print('Item number: ' + str(number))
        print(processor_brand[0].text)
        print(processor_name[0].get('content'))
        print(processor_price[0].text)
        number += 1


one = get_processor_links()
get_processor_data(one)
