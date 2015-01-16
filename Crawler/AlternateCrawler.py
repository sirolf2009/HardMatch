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


def get_hardware_page_url(url, search_words):
    """Every <a> with 'search words' as text"""
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


def get_subLevel2_url(hardware_page_url, url, component_search_words):
    """get all <a> with subLevel2 class"""
    source_code = requests.get(hardware_page_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    subLevel2_urls = []
    for subLevel2_url in soup.find_all('li', class_="subLevel2"):
            for list_item in component_search_words:
                if list_item in subLevel2_url.text:
                    href = subLevel2_url.a['href']
                    subLevel2_url_full = url + href
                    subLevel2_urls.append(subLevel2_url_full)
    finished_list = list(set(subLevel2_urls))
    return finished_list


def get_subLevel3_url(subLevel2_urls, url, component_search_words):
    """get all <a> with subLevel3 class"""
    subLevel3_urls = []
    for subLevel2_url in subLevel2_urls:
        source_code = requests.get(subLevel2_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for subLevel3_url in soup.findAll('li', class_="subLevel3"):
            for list_item in component_search_words:
                if list_item in subLevel3_url.text:
                    href = subLevel3_url.a['href']
                    subLevel3_url_full = url + href
                    subLevel3_urls.append(subLevel3_url_full)
    return subLevel3_urls


def get_subLevel4_url(subLevel3_urls, url, component_search_words):
    """get all <a> with subLevel3 class"""
    subLevel4_urls = []
    for subLevel3_url in subLevel3_urls:
        source_code = requests.get(subLevel3_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for subLevel4_url in soup.findAll('li', class_="subLevel4"):
            for list_item in component_search_words:
                if list_item in subLevel4_url.text:
                    href = subLevel4_url.a['href']
                    subLevel4_url_full = url + href
                    subLevel4_urls.append(subLevel4_url_full)
    return subLevel4_urls


def get_all_product_links(links_l4, url):
    list_of_links = []
    for link_l4 in links_l4:
        source_code = requests.get(link_l4)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for item in soup.find_all('a', class_='productLink'):
            href = item['href']
            full_link = url + href
            print(full_link)
            list_of_links.append(full_link)
        return list_of_links

# def parser_and_object_creator:


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

        if not component_brand:
            component_brand_string = 'NULL'
        else:
            component_brand_string = component_brand[0].text

        if not component_name:
            component_name_string = 'NULL'
        else:
            component_name_string = component_brand[0].text

        if not component_price:
            component_price_text = 'NULL'
        else:
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
        # Component.print_property(component)


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


behuizing = ['Behuizingen']
geheugen = ["Geheugen"]
grafische_kaarten = ['Grafische kaarten']
opslag = ['Harde schijven intern']
koeling = ['Koeling']
moederborden = ['Moederborden']
processors = ['Processoren']

behuizing_L3 = ['Desktop']
geheugen_L3 = ['']
grafische_kaarten_L3 = ["PCIe kaarten Matrox", "AGP kaarten", "PCI kaarten"]
opslag_L3 = ["SATA", "SAS", "Hybride", "SSD's"]
koeling_L3 = ["CPU"]
moederborden_L3 = ["AMD", "Intel"]
processors_L3 = ["Desktop"]

processors_L4 = ["Alles bekijken"]

neo4j_db = neo4j.Graph("http://localhost:7474/db/data/")
store = Node('Store', name='alternate.nl')
neo4j_db.create(store)

url = "http://www.alternate.nl"
hardware = "http://www.alternate.nl/html/highlights/page.html?tk=7&lk=7&hgid=189&tgid=906"

behuizing_output = get_subLevel2_url(hardware, url, behuizing)
behuizing_sublinks = get_subLevel3_url(behuizing_output, url, behuizing_L3)
all_behuizing = get_all_product_links(behuizing_sublinks, url)

# geheugen_output = get_subLevel2_url(hardware, url, geheugen)
# print("Geheugen:")
# print(geheugen_output)

grafische_kaarten_output = get_subLevel2_url(hardware, url, grafische_kaarten)
grafische_kaarten_sublinks = get_subLevel3_url(grafische_kaarten_output, url, grafische_kaarten_L3)
all_grafische_kaarten = get_all_product_links(grafische_kaarten_sublinks, url)

opslag_output = get_subLevel2_url(hardware, url, opslag)
opslag_sublinks = get_subLevel3_url(opslag_output, url, opslag_L3)
all_opslag = get_all_product_links(opslag_sublinks, url)

koeling_output = get_subLevel2_url(hardware, url, koeling)
koeling_output_sublinks = get_subLevel3_url(koeling_output, url, koeling_L3)
all_koeling = get_all_product_links(koeling_output_sublinks, url)

moederborden_output = get_subLevel2_url(hardware, url, moederborden)
moederborden_output_sublinks = get_subLevel3_url(moederborden_output, url, moederborden_L3)
all_moederborden = get_all_product_links(moederborden_output_sublinks, url)

processors_output = get_subLevel2_url(hardware, url, processors)
processors_output_sublinks = get_subLevel3_url(processors_output, url, processors_L3)
processors_output_sublinks_l4 = get_subLevel4_url(processors_output_sublinks, url, processors_L4)
all_processors = get_all_product_links(processors_output_sublinks_l4, url)

print(len(all_behuizing) + len(all_grafische_kaarten) +
      len(all_koeling) + len(all_moederborden) + len(all_opslag) +
      len(all_processors))