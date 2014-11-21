#WebCrawler Prototype

__author__ = "Rene van der Horst"
__copyright__ = "Copyright 2014, HardMatch Project"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

#Indentation: 4 spaces
#Variable naming: skeleton case

#This program picks up data from alternate.nl

import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, node, rel, Node, Relationship

neo4j_db = neo4j.Graph("http://localhost:7474/db/data/")
store = Node(type='Store', Naam='alternate.nl')
neo4j_db.create(store)

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
        processor_socket_type = url_soup.find_all('td', {'class': 'techDataSubCol techDataSubColValue'})

        processor_name_string = processor_name[0].get('content')
        processor_price_string = processor_price[0].text
        processor_socket_type_string = processor_socket_type[0].get('content')

        print(processor_name_string)
        print(processor_price_string)
        print(processor_socket_type_string)

        neo4j_db.create(
            node("Component", "CPU", {"name": processor_name_string}, {"Socket Type": processor_socket_type_string}),
            node("Store", {"name": "alternate.nl"}),
            rel(0, "SOLD_AT", 1, {"price": processor_price_string})
        )

        number += 1

one = get_processor_links()
get_processor_data(one)


class ComponentAndRelationship():

    properties = {}  # Dictionary

    def add_property(self, key, value):
        self.properties[key] = value

    def print_property(self):
        for x in self.properties:
            print(x)
            print(self.properties[x])

    def save_component(self):
        component = Node(naam=self.properties['Naam'])
        neo4j_db.pull()
        for i in self.properties:
            component.properties[i] = self.properties[i]
        neo4j_db.create(component)

        relationship = Relationship(self, 'SOLD_AT', store, price=self.properties['price'])
        neo4j_db.create(relationship)

    '''
    def save_relationship(self, store):
        relationship = Relationship(self, 'SOLD_AT', store, price=self.properties['price'])
        neo4j_db.create(relationship)
    '''