#WebCrawler.py
__author__ = "Rene van der Horst"
__copyright__ = "Copyright 2014, HardMatch Project"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, Node, Relationship


def get_page_soup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup


def source_code_to_soup(source_code):
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup


def get_hardware_page_url(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    hardware_page_url = 'none'
    for tab in soup.findAll('a', {'class': 'tab'}):
        if tab.text == 'Hardware':
            hardware_page_path = tab.get('href')
            hardware_page_url = url + hardware_page_path
    return hardware_page_url


def get_component_page_url(hardware_page_url, url):
    source_code = requests.get(hardware_page_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    component_page_url = "none"
    for anchor in soup.findAll('a', {'target': '_self'}):
        if anchor.text == 'Processoren':
            component_page_path = anchor.get('href')
            component_page_url = url + component_page_path
    return component_page_url


def get_component_links(component_page_url, url):
    source_code = requests.get(component_page_url)
    plain_text = source_code.text
    component_page_soup = BeautifulSoup(plain_text)
    component_links = []
    for component in component_page_soup.findAll('a', {'class': 'h1x1'}):
        link = component.get('href')
        full_link = url + link
        component_links.append(full_link)
    return component_links


def get_component_object(component_links):
    component_mhz = "none"
    for component_link in component_links:
        url_source_code = requests.get(component_link)
        url_plain_text = url_source_code.text
        component_soup = BeautifulSoup(url_plain_text)

        component_brand = component_soup.find_all('span', {'itemprop': 'brand'})
        component_name = component_soup.find_all('meta', {'itemprop': 'name'})
        component_price = component_soup.find_all('span', {'itemprop': 'price'})
        for component in component_soup.find_all('td', {'class': 'techDataSubCol techDataSubColValue'}):
            if 'MHz' in str(component):
                component_mhz = component.text
                break

        component_brand_string = component_brand[0].text
        component_name_string = component_name[0].get('content')
        component_price_string = component_price[0].text

        component = Component()
        Component.add_property(component, 'brand', component_brand_string)
        Component.add_property(component, 'name', component_name_string)
        Component.add_property(component, 'price', component_price_string)
        Component.add_property(component, 'MHz', component_mhz)
        Component.save_component_with_relationships(component)
        Component.print_property(component)


class Component():

    properties = {}  # Dictionary

    def add_property(self, key, property):
        self.properties[key] = property

    def print_property(self):
        for key in self.properties:
            print("x: " + key)
            print("p: " + self.properties[key])

    def save_component_with_relationships(self):
        component = Node("component")
        for key in self.properties:
            component.properties[key] = self.properties[key]
        store.pull()
        relationship = Relationship(component, 'SOLD_AT', store, price=self.properties['price'])
        neo4j_db.create(component)
        neo4j_db.create(relationship)


neo4j_db = neo4j.Graph("http://localhost:7474/db/data/")
store = Node(type='Store', name='alternate.nl')
neo4j_db.create(store)

url = "http://www.alternate.nl"
hardware = get_hardware_page_url(url)
components = get_component_page_url(hardware, url)
links = get_component_links(components, url)
get_component_object(links)


#component_socket_type = component_soup.find_all('td', {'class': 'techDataSubCol techDataSubColValue'})
#component_clock_speed = component_soup.find_all('td', {'class': 'techDataSubCol techDataSubColValue'})

#component_socket_type_string = component_socket_type[0].get('content')
#component_clock_speed_string = component_clock_speed[0].get('content')