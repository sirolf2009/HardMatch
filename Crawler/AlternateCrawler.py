__author__ = "Rene van der Horst"
__copyright__ = "Copyright 2014, HardMatch Project"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

import requests
from bs4 import BeautifulSoup
from py2neo import neo4j, Node, Relationship
from Crawler import components


def get_components():
    components = Category('Components', ['Componenten', 'Hardware'])
    return components


def get_categories():
    graphics_cards = Category('Graphics Cards', ['Grafische kaarten', 'grafische kaarten'])
    processors = Category('Processors', ['Processoren', 'processoren'])
    motherboards = Category('Motherboards', ['Moederborden', 'moederborden'])
    memory_chips = Category('RAM', ['Geheugenkaarten', 'RAM', 'ram'])
    # cases = Category('Cases', ['Behuizingen'])
    solid_state_drives = Category('Solid State Drives', ['SSD', 'ssd'])
    hard_drives = Category('Hard Drives', ['Harde schijven intern', 'harde schijven intern'])

    categories = [graphics_cards,
                  processors,
                  motherboards,
                  memory_chips,
                  solid_state_drives,
                  hard_drives]
    return categories


def get_page_soup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup


def source_code_to_soup(source_code):
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup


def get_hardware_page_url(url, search_words):
    """Top Level"""
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    hardware_page_url = "none"
    for component in range(len(search_words.titles)):
        for tab in soup.findAll('a', {'class': 'tab'}):
            if tab.text in search_words.titles[component]:
                hardware_page_path = tab.get('href')
                hardware_page_url = url + hardware_page_path
                break
    return hardware_page_url


def get_component_page_url(hardware_page_url, url, categories):
    """Mid Level"""
    source_code = requests.get(hardware_page_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    component_page_url_list = []
    for anchor in soup.findAll('a', {'target': '_self'}):
        for category in range(len(categories)):
            for categoryTitle in range(len(categories[category].getTitles())):
                if anchor.text in categories[category].getTitle(categoryTitle):
                    component_page_path = anchor.get('href')
                    component_page_url = url + component_page_path
                    component_page_url_list.append(component_page_url)
    return component_page_url_list


def get_component_url(component_page_url_list, url):
    """Low Level"""
    component_links = []
    for component_page_url in component_page_url_list:
        source_code = requests.get(component_page_url)
        plain_text = source_code.text
        component_page_soup = BeautifulSoup(plain_text)
        for component in component_page_soup.findAll('a', {'class': 'h1x1'}):
            link = component.get('href')
            full_link = url + link
            print(full_link)
            component_links.append(full_link)
    return component_links


def get_motherboard_object(component_links):
    for component_link in component_links:
        if 'moederbord' in component_link:
            print("motherboard")
    test = components.RAM()
    return "MB"


def get_graphics_card_object(component_links):
    for component_link in component_links:
        if 'grafische' in component_link:
            print("graphics card")
    # test = components.GraphicsCard
    return "GC"


def get_processor_object(component_links):
    for component_link in component_links:
        if 'processor' in component_link:
            print("processor")
    return "Pro"


def get_memory_object(component_links):
    for component_link in component_links:
        if 'geheugen' in component_link:
            print("memory")
        return "Mem"


def get_ssd_object(component_links):
    for component_link in component_links:
        if 'SSD' in component_link:
            print("SSD")
    return "SSD"


def get_hd_object(component_links):
    for component_link in component_links:
        if 'harde' in component_link:
            print("HD")
    return "HD"


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
        component_price_text = component_price[0].text

        def create_price_string(input_price):
            new_string = input_price.replace("€", ""). \
                replace("*", "").replace(" ", ""). \
                replace(",", ".").replace("-", "00")
            return new_string

        component_price_string = create_price_string(component_price_text)

        component = Component()
        Component.add_property(component, 'brand', component_brand_string)
        Component.add_property(component, 'name', component_name_string)
        Component.add_relationship_property(component, 'price', component_price_string)
        Component.add_property(component, 'processor speed', component_mhz)
        Component.save_component_with_relationships(component)
        Component.print_property(component)


class Component():
    properties = {}
    relationship_properties = {}

    def add_property(self, key, property):
        self.properties[key] = property

    def add_relationship_property(self, key, property):
        self.relationship_properties[key] = property

    def print_property(self):
        for key in self.properties:
            print("x: " + key)
            print("p: " + self.properties[key])

    def save_component_with_relationships(self):
        component = Node("Component", "CPU")
        for key in self.properties:
            component.properties[key] = self.properties[key]
        store.pull()
        relationship = Relationship(component, 'SOLD_AT', store, price=self.relationship_properties['price'])
        neo4j_db.create(component)
        neo4j_db.create(relationship)


class Category():
    name = ''
    titles = []

    def __init__(self, name, titles):
        self.name = name
        self.titles = list(titles)

    def set_name(self, name):
        self.name = name

    def set_titles(self, titles):
        self.titles = list(titles)

    def get_name(self):
        return self.name

    def get_title(self, index):
        return self.titles[index]

    def get_titles(self):
        return self.titles

    def print_category(self):
        print(self.name)
        for i in range(len(self.titles)):
            print(self.titles[i])


neo4j_db = neo4j.Graph("http://localhost:7474/db/data/")
store = Node('Store', name='alternate.nl')
neo4j_db.create(store)

url = "http://www.alternate.nl"
hardware = get_hardware_page_url(url, get_components())
components_list = get_component_page_url(hardware, url, get_categories())
links = get_component_url(components_list, url)
motherboards = get_motherboard_object(links)
graphics_cards = get_graphics_card_object(links)
processors = get_processor_object(links)
memory_cards = get_memory_object(links)
SSD = get_ssd_object(links)
HD = get_hd_object(links)

get_component_object(links)


# component_socket_type = component_soup.find_all('td', {'class': 'techDataSubCol techDataSubColValue'})
# component_clock_speed = component_soup.find_all('td', {'class': 'techDataSubCol techDataSubColValue'})

# component_socket_type_string = component_socket_type[0].get('content')
# component_clock_speed_string = component_clock_speed[0].get('content')