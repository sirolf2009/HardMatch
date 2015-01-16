__author__ = "Rene van der Horst"
__copyright__ = "Copyright 2014, HardMatch Project"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

import requests, re
from bs4 import BeautifulSoup
from py2neo import neo4j, Node, Relationship
from pymongo import MongoClient

import IParseSave


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
            # print(full_link)
            list_of_links.append(full_link)
        return list_of_links

# def parser_and_object_creator:


def get_CPU(detail_pages):
    label = 'CPU'
    cpu = IParseSave.CPU()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        link = detail_page
        # MODELID
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            cpu.properties['ModelID'] = modelID
        except AttributeError:
            print("NULL")
        # NAME
        try:
            name = soup.find('meta', {"itemprop": "name"})
            cpu.properties['Name'] = name['content'].encode('utf-8')
        except AttributeError:
            print("NULL")
        # BRAND
        try:
            brand = soup.find('meta', {"itemprop": "brand"})
            cpu.properties['Merk'] = brand
        except AttributeError:
            print("NULL")
        # Serie
        try:
            serie = soup.find('td', text="Socket").next_sibling.text
            cpu.properties['Serie'] = serie
        except AttributeError:
            print("NULL")
        # Socket
        try:
            socket = soup.find('td', text="Socket").next_sibling.text
            cpu.properties['Socket'] = socket
        except AttributeError:
            print("NULL")
        # Amount of Cores
        try:
            aantal_cores = soup.find('td', text="Aantal").next_sibling.text
            cpu.properties['AantalCores'] = aantal_cores
        except AttributeError:
            print("NULL")
        # Snelheid
        try:
            snelheid = soup.find('td', text="CPU snelheid").next_sibling.text
            cpu.properties['Snelheid'] = snelheid
        except AttributeError:
            print("NULL")
        # Geheugenspecificatie
        try:
            geheugen_specificatie = soup.find('td', text="Standaarden").next_sibling.text
            cpu.properties['GeheugenSpecificatie'] = geheugen_specificatie
        except AttributeError:
            print("NULL")
        # CPU cache level 1
        try:
            CPU_cache_level1 = soup.find('td', text="L1").next_sibling.text
            cpu.properties['CPUCacheLevel1'] = CPU_cache_level1
        except AttributeError:
            print("NULL")
        # CPU cache level 2
        try:
            CPU_cache_level2 = soup.find('td', text="L2").next_sibling.text
            cpu.properties['CPUCacheLevel2'] = CPU_cache_level2
        except AttributeError:
            print("NULL")
        # Price
        try:
            x = soup.find('span', {"itemprop": "price"}) # DUURT HEEL LANG !
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"
        # Shipping costs
        try:
            x = soup.find('div', {"id": "cheapestShippingCosts"})
            shipping_costs = price_parser(x.text)
        except AttributeError:
            shipping_costs = "NULL"

        inStock = "NULL"
        # link = cpu.properties
        # print(cpu.properties)
        saveComponent(cpu.properties, label, price, inStock, link)


def get_Motherboard(detail_pages):
    label = 'Motherboard'
    motherboard = IParseSave.Motherboard()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        link = detail_page
        # MODELID
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            motherboard.properties['ModelID'] = modelID
        except AttributeError:
            motherboard.properties['ModelID'] = "NULL"
        # NAME
        try:
            name = soup.find('meta', {"itemprop": "name"})
            motherboard.properties['Name'] = name['content'].encode('utf-8')
        except AttributeError:
            motherboard.properties['Name'] = "NULL"
        # BRAND
        try:
            brand = soup.find('meta', {"itemprop": "brand"})
            motherboard.properties['Merk'] = brand
        except AttributeError:
            motherboard.properties['Merk'] = "NULL"
        # Socket
        try:
            socket = soup.find('td', {"class": "c1"}, text='Socket')
            print(socket)
            print(socket.next_elements)
            motherboard.properties['Socket'] = socket
        except AttributeError:
            motherboard.properties['Socket'] = "NULL"
        # amount of Sockets
        try:
            amount_of_sockets = soup.find('td', text="Maximaal ondersteunde CPU's").next_sibling.text
            motherboard.properties['AantalSockets'] = amount_of_sockets
        except AttributeError:
            motherboard.properties['AantalSockets'] = "NULL"
        # Form Factor
        try:
            FormFactor = soup.find('td', text="Formfactor").next_sibling.text
            motherboard.properties['FormFactor'] = FormFactor
        except AttributeError:
            motherboard.properties['FormFactor'] = "NULL"

        # 'BIOSofUEFI': 'null',
        # 'DualofSingleBIOSUEFI': 'null',
        # 'Moederbordchipset': 'null'

        # Geheugentype
        try:
            geheugen_type = soup.find('td', text="Geheugen type").next_sibling.text
            motherboard.properties['Geheugentype'] = geheugen_type
        except AttributeError:
            motherboard.properties['Geheugentype'] = "NULL"
        # 'MaximumGeheugengrootte': 'null',
        # 'HardeschijfBus': 'null',
        # CardInterface
        try:
            card_interface = soup.find('td', text="Sloten").next_sibling.text
            motherboard.properties['CardInterface'] = card_interface
        except AttributeError:
            motherboard.properties['CardInterface'] = "NULL"
        # Snelheid
        try:
            snelheid = soup.find('td', text="CPU snelheid").next_sibling.text
            motherboard.properties['Snelheid'] = snelheid
        except AttributeError:
            motherboard.properties['Snelheid'] = "NULL"
        # Geheugenspecificatie
        try:
            geheugen_specificatie = soup.find('td', text="Standaarden").next_sibling.text
            motherboard.properties['GeheugenSpecificatie'] = geheugen_specificatie
        except AttributeError:
           motherboard.properties['GeheugenSpecificatie'] = "NULL"
        # CPU cache Level 1
        try:
            CPU_cache_level1 = soup.find('td', text="L1").next_sibling.text
            motherboard.properties['CPUCacheLevel1'] = CPU_cache_level1
        except AttributeError:
            motherboard.properties['CPUCacheLevel1'] = "NULL"
        # CPU cache Level 2
        try:
            CPU_cache_level2 = soup.find('td', text="L2").next_sibling.text
            motherboard.properties['CPUCacheLevel2'] = CPU_cache_level2
        except AttributeError:
            motherboard.properties['CPUCacheLevel2'] = "NULL"
        # price
        try:
            x = soup.find('span', {"itemprop": "price"}) # DUURT HEEL LANG !
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"
        #
        try:
            x = soup.find('div', {"id": "cheapestShippingCosts"})
            shipping_costs = price_parser(x.text)
        except AttributeError:
            shipping_costs = "NULL"

        inStock = "NULL"
        # link = cpu.properties
        # print(motherboard.properties)
        saveComponent(motherboard.properties, label, price, inStock, link)


def price_parser(line):
    x = line.replace("€", "").\
        replace("*", "").\
        replace(",", ".").\
        replace(" ", "").\
        replace("verzendkosten", "").\
        replace("va.", "")
    return x


def saveComponent(properties, label, price, voorraad, link):
    neo4j_db = neo4j.Graph("http://localhost:7474/db/data/")
    modelID = properties['ModelID']

    if bool(neo4j_db.cypher.execute_one('match (n) where n.ModelID = "{}" return n'.format(modelID))):
        cn = neo4j_db.cypher.execute_one('match (n) where n.ModelID = "{}" return n'.format(modelID))
    else:
        cn = Node(label)
        for i in properties:
            cn.properties[i] = properties[i]
        neo4j_db.create(cn)
        cn.add_labels('Component')
        cn.push()

    rel = Relationship(cn, 'SOLD_AT', store, price=price, in_stock=voorraad, link=link)
    neo4j_db.create(rel)

neo4j_db = neo4j.Graph("http://localhost:7474/db/data/")

if not bool(neo4j_db.cypher.execute_one('MATCH (node {name: "alternate.nl"}) RETURN node')):
    store = Node('Store', name='www.alternate.nl')
    neo4j_db.create(store)


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
get_CPU(all_processors)
# get_Motherboard(all_moederborden)

print(len(all_behuizing) + len(all_grafische_kaarten) +
      len(all_koeling) + len(all_moederborden) + len(all_opslag) +
      len(all_processors))
