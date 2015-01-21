__author__ = "Rene van der Horst"
__copyright__ = "Copyright 2014, HardMatch Project"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

import time
import requests, re
from datetime import datetime
from bs4 import BeautifulSoup
from py2neo import neo4j, Node, Relationship
from pymongo import MongoClient

import IParseSave


client = MongoClient('localhost', 27017)
mongodb = client.alternate


class store_object():
    def create_store(self, name, storeUrl):
        n = Node(name, Name=storeUrl)
        return n

neo4j_db = neo4j.Graph("http://localhost:7474/db/data/")


if bool(neo4j_db.cypher.execute_one('MATCH(n:Store) WHERE n.Name = "www.alternate.nl" RETURN n')):
    pass
else:
    store = store_object.create_store(store_object(), 'Store', 'www.alternate.nl')
    neo4j_db.create(store)

store = neo4j_db.cypher.execute_one('MATCH(n:Store) WHERE n.Name = "www.alternate.nl" RETURN n')


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
            list_of_links.append(full_link)
        return list_of_links


def get_CPU(detail_pages):
    label = 'CPU'
    cpu = IParseSave.CPU()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        link = detail_page
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            print(modelID)
            cpu.properties['ModelID'] = modelID
        except AttributeError:
            cpu.properties['ModelID'] = "NULL"
        try:
            brand = soup.find('span', {"itemprop": "brand"}).text
            cpu.properties['Merk'] = brand
        except AttributeError:
            cpu.properties['Merk'] = "NULL"
        try:
            name = soup.find('meta', {"itemprop": "name"})
            x = name['content'].encode('utf-8').text
            sep = ','
            rest = x.split(sep, 1)[0].replace("b'", "")
            final = brand + " " + rest
            cpu.properties['Name'] = final
        except AttributeError:
            cpu.properties['Name'] = "NULL"
        try:
            serie = soup.find('td', text="Socket").next_sibling.text
            cpu.properties['Serie'] = serie
        except AttributeError:
            cpu.properties['Serie'] = "NULL"
        try:
            aantal_cores = soup.find('td', text="Aantal").next_sibling.text
            cpu.properties['AantalCores'] = aantal_cores
        except AttributeError:
            cpu.properties['AantalCores'] = "NULL"
        try:
            snelheid = soup.find('td', text="CPU snelheid").next_sibling.text
            cpu.properties['Snelheid'] = snelheid
        except AttributeError:
            cpu.properties['Snelheid'] = "NULL"
        try:
            geheugen_specificatie = soup.find('td', text="Standaarden").next_sibling.text
            cpu.properties['GeheugenSpecificatie'] = geheugen_specificatie
        except AttributeError:
            cpu.properties['GeheugenSpecificatie'] = "NULL"
        try:
            CPU_cache_level1 = soup.find('td', text="L1").next_sibling.text
            cpu.properties['CPUCacheLevel1'] = CPU_cache_level1
        except AttributeError:
           cpu.properties['CPUCacheLevel1'] = "NULL"
        try:
            CPU_cache_level2 = soup.find('td', text="L2").next_sibling.text
            cpu.properties['CPUCacheLevel2'] = CPU_cache_level2
        except AttributeError:
            cpu.properties['CPUCacheLevel2'] = "NULL"
        try:
            x = soup.find('span', {"itemprop": "price"})
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"
        try:
            x = soup.find('div', {"class": "availability"})
            InStock = x.p.text
        except AttributeError:
            InStock = "NULL"

        saveComponent(cpu.properties, label, price, InStock, link)


def get_Motherboard(detail_pages):
    label = 'Motherboard'
    motherboard = IParseSave.Motherboard()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        table = soup.table
        link = detail_page
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            motherboard.properties['ModelID'] = modelID
        except AttributeError:
            motherboard.properties['ModelID'] = "NULL"
        try:
            name = soup.find('meta', {"itemprop": "name"})
            motherboard.properties['Name'] = name['content'].encode('utf-8')
        except AttributeError:
            motherboard.properties['Name'] = "NULL"
        try:
            brand = soup.find('meta', {"itemprop": "brand"})
            motherboard.properties['Merk'] = brand
        except AttributeError:
            motherboard.properties['Merk'] = "NULL"
        try:
            socket = table.find('td', {"class": "c4"}).text
            motherboard.properties['Socket'] = socket
        except AttributeError:
            motherboard.properties['Socket'] = "NULL"
        try:
            amount_of_sockets = soup.find('td', text="Maximaal ondersteunde CPU's").next_sibling.text
            motherboard.properties['AantalSockets'] = amount_of_sockets
        except AttributeError:
            motherboard.properties['AantalSockets'] = "NULL"
        try:
            tr_tag = table.find('td', {"class": "c1"}, text="Formfactor").parent
            form_factor = tr_tag.findNext('td', {"class": "c4"}).text
            motherboard.properties['FormFactor'] = form_factor
        except AttributeError:
            motherboard.properties['FormFactor'] = "NULL"
        try:
            tr_tag = table.find('td', {"class": "c2"}, text="Type geheugen")
            geheugen_type = tr_tag.findNext('td', {"class": "c4"}).text
            motherboard.properties['Geheugentype'] = geheugen_type
        except AttributeError:
            motherboard.properties['Geheugentype'] = "NULL"
        try:
            tr_tag = soup.find('td', text="Sloten").parent
            card_interface = tr_tag.findNext('td', {"class": "c4"}).text
            motherboard.properties['CardInterface'] = card_interface
        except AttributeError:
            motherboard.properties['CardInterface'] = "NULL"
        try:
            snelheid = soup.find('td', text="CPU snelheid").next_sibling.text
            motherboard.properties['Snelheid'] = snelheid
        except AttributeError:
            motherboard.properties['Snelheid'] = "NULL"
        try:
            geheugen_specificatie = soup.find('td', text="Standaarden").next_sibling.text
            motherboard.properties['GeheugenSpecificatie'] = geheugen_specificatie
        except AttributeError:
           motherboard.properties['GeheugenSpecificatie'] = "NULL"
        try:
            CPU_cache_level1 = soup.find('td', text="L1").next_sibling.text
            motherboard.properties['CPUCacheLevel1'] = CPU_cache_level1
        except AttributeError:
            motherboard.properties['CPUCacheLevel1'] = "NULL"
        try:
            CPU_cache_level2 = soup.find('td', text="L2").next_sibling.text
            motherboard.properties['CPUCacheLevel2'] = CPU_cache_level2
        except AttributeError:
            motherboard.properties['CPUCacheLevel2'] = "NULL"
        try:
            x = soup.find('span', {"itemprop": "price"})
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"
        try:
            x = soup.find('div', {"id": "cheapestShippingCosts"})
            shipping_costs = price_parser(x.text)
        except AttributeError:
            shipping_costs = "NULL"
        try:
            x = soup.find('div', {"class": "availability"})
            InStock = x.p.text
        except AttributeError:
            InStock = "NULL"

        saveComponent(motherboard.properties, label, price, InStock, link)


def get_CPU_Fan(detail_pages):
    label = 'CPUFan'
    cpu_fan = IParseSave.CPUFan()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        table = soup.find('table', {'class': 'techDataTable'})
        link = detail_page
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            cpu_fan.properties['ModelID'] = modelID
        except AttributeError:
            cpu_fan.properties['ModelID'] = "NULL"
        try:
            name = soup.find('meta', {"itemprop": "name"})
            cpu_fan.properties['Name'] = name['content'].encode('utf-8')
        except AttributeError:
            cpu_fan.properties['Name'] = "NULL"
        try:
            brand = soup.find('meta', {"itemprop": "brand"})
            cpu_fan.properties['Merk'] = brand
        except AttributeError:
            cpu_fan.properties['Merk'] = "NULL"
        try:
            tr_tag = table.find('td', {"class": "techDataCol1"}, text="Socket")
            text = tr_tag.parent.table.tr.text
            socket = text[4:]
            cpu_fan.properties['Socket'] = socket
        except AttributeError:
            cpu_fan.properties['Socket'] = "NULL"
        try:
            x = soup.find('span', {"itemprop": "price"})
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"
        try:
            x = soup.find('div', {"id": "cheapestShippingCosts"})
            shipping_costs = price_parser(x.text)
        except AttributeError:
            shipping_costs = "NULL"
        try:
            x = soup.find('div', {"class": "availability"})
            InStock = x.p.text
        except AttributeError:
            InStock = "NULL"

        saveComponent(cpu_fan.properties, label, price, InStock, link)


def get_RAM(detail_pages):
    label = 'RAM'
    ram = IParseSave.RAM()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        table = soup.find('div', {'class': 'techData'})
        link = detail_page
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            ram.properties['ModelID'] = modelID
        except AttributeError:
            ram.properties['ModelID'] = "NULL"
        try:
            name = soup.find('meta', {"itemprop": "name"})
            ram.properties['Name'] = name['content'].encode('utf-8')
        except AttributeError:
            ram.properties['Name'] = "NULL"
        try:
            brand = soup.find('meta', {"itemprop": "brand"})
            ram.properties['Merk'] = brand
        except AttributeError:
            ram.properties['Merk'] = "NULL"
        try:
            x = table.find('td', {"class": "c1"}, text="Type")
            type = x.parent.findNext('td', {"class": "c4"}).text
            ram.properties['GeheugenType'] = type
        except AttributeError:
            ram.properties['GeheugenType'] = "NULL"
        try:
            x = soup.find('span', {"itemprop": "price"})
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"
        try:
            x = soup.find('div', {"id": "cheapestShippingCosts"})
            shipping_costs = price_parser(x.text)
        except AttributeError:
            shipping_costs = "NULL"
        try:
            x = soup.find('div', {"class": "availability"})
            InStock = x.p.text
        except AttributeError:
            InStock = "NULL"

        saveComponent(ram.properties, label, price, InStock, link)


def get_Case(detail_pages):
    label = 'Case'
    cpu_fan = IParseSave.Case()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        table = soup.find('table', {'class': 'techDataTable'})
        link = detail_page
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            cpu_fan.properties['ModelID'] = modelID
        except AttributeError:
            cpu_fan.properties['ModelID'] = "NULL"
        try:
            name = soup.find('meta', {"itemprop": "name"})
            cpu_fan.properties['Name'] = name['content'].encode('utf-8')
        except AttributeError:
            cpu_fan.properties['Name'] = "NULL"
        try:
            brand = soup.find('meta', {"itemprop": "brand"})
            cpu_fan.properties['Merk'] = brand
        except AttributeError:
            cpu_fan.properties['Merk'] = "NULL"
        try:
            tr_tag = table.find('td', {"class": "techDataCol1"}, text="Formaat")
            form_factor = tr_tag.parent.table.tr.text
            cpu_fan.properties['FormFactor'] = form_factor
        except AttributeError:
            cpu_fan.properties['FormFactor'] = "NULL"
        try:
            x = soup.find('span', {"itemprop": "price"})
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"
        try:
            x = soup.find('div', {"id": "cheapestShippingCosts"})
            shipping_costs = price_parser(x.text)
        except AttributeError:
            shipping_costs = "NULL"
        try:
            x = soup.find('div', {"class": "availability"})
            InStock = x.p.text
        except AttributeError:
            InStock = "NULL"

        saveComponent(cpu_fan.properties, label, price, InStock, link)


def get_Storage(detail_pages):
    label = 'Storage'
    case = IParseSave.Storage()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        table = soup.find('table', {'class': 'techDataTable'})
        link = detail_page
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            case.properties['ModelID'] = modelID
        except AttributeError:
            case.properties['ModelID'] = "NULL"
        try:
            name = soup.find('meta', {"itemprop": "name"})
            case.properties['Name'] = name['content'].encode('utf-8')
        except AttributeError:
            case.properties['Name'] = "NULL"
        try:
            brand = soup.find('meta', {"itemprop": "brand"})
            case.properties['Merk'] = brand
        except AttributeError:
            case.properties['Merk'] = "NULL"
        try:
            tr_tag = table.find('td', {"class": "techDataCol1"}, text="Capaciteit")
            text = tr_tag.parent.table.tr.text
            # socket = text[4:]
            case.properties['Opslagcapactiteit'] = text
        except AttributeError:
            case.properties['Socket'] = "NULL"
        try:
            x = soup.find('span', {"itemprop": "price"})
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"
        try:
            x = soup.find('div', {"id": "cheapestShippingCosts"})
            shipping_costs = price_parser(x.text)
        except AttributeError:
            shipping_costs = "NULL"
        try:
            x = soup.find('div', {"class": "availability"})
            InStock = x.p.text
        except AttributeError:
            InStock = "NULL"

        saveComponent(case.properties, label, price, InStock, link)


def get_GPU(detail_pages):
    label = 'GraphicsCard'
    graphicsCard = IParseSave.GraphicsCard()
    for detail_page in detail_pages:
        source_code = requests.get(detail_page)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        table = soup.find('table', {'class': 'techDataTable'})
        link = detail_page
        try:
            x = soup.find('meta', {"itemprop": "name"})
            modelID = x['content'].replace('"', "")
            graphicsCard.properties['ModelID'] = modelID
        except AttributeError:
            graphicsCard.properties['ModelID'] = "NULL"
        try:
            name = soup.find('meta', {"itemprop": "name"})
            graphicsCard.properties['Name'] = name['content'].encode('utf-8')
        except AttributeError:
            graphicsCard.properties['Name'] = "NULL"
        try:
            brand = soup.find('meta', {"itemprop": "brand"})
            graphicsCard.properties['Merk'] = brand
        except AttributeError:
            graphicsCard.properties['Merk'] = "NULL"
        try:
            tr_tag = table.find('td', text="Type")
            text = tr_tag.parent.table.tr.text
            graphicsCard.properties['GeheugenType'] = text
        except AttributeError:
            graphicsCard.properties['Socket'] = "NULL"
        try:
            tr_tag = table.find('td', text="Aansluiting")
            text = tr_tag.parent.table.tr.text
            graphicsCard.properties['CardInterface'] = text
        except AttributeError:
            graphicsCard.properties['Socket'] = "NULL"
        try:
            x = soup.find('span', {"itemprop": "price"})
            price = price_parser(x.text)
        except AttributeError:
            price = "NULL"

        try:
            x = soup.find('div', {"id": "cheapestShippingCosts"})
            shipping_costs = price_parser(x.text)
        except AttributeError:
            shipping_costs = "NULL"
        try:
            x = soup.find('div', {"class": "availability"})
            InStock = x.p.text
        except AttributeError:
            InStock = "NULL"

        saveComponent(graphicsCard.properties, label, price, InStock, link)


def price_parser(line):
    x = line.replace("€", "").\
        replace("*", "").\
        replace(",", ".").\
        replace(" ", "").\
        replace("verzendkosten", "").\
        replace("va.", "")
    return x


def saveComponent(properties, label, price, voorraad, link):
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

    rel = Relationship(cn, 'SOLD_AT', store, Price=price, InStock=voorraad, productUrl=link)
    neo4j_db.create(rel)

    # MongoDB
    now = datetime.now()

    post = {'ModelID': properties['ModelID'],
            'Name': properties['Name'],
            'Price': price,
            'Brand': properties['Merk'],
            'Type': label,
            'Timestamp': int(time.mktime(now.timetuple()))}

    if label == 'CPU': mongodb.CPU.insert(post)
    elif label == 'Motherboard': mongodb.Motherboard.insert(post)
    elif label == 'CPUFan': mongodb.CPUFan.insert(post)
    elif label == 'GraphicsCard': mongodb.GraphicsCard.insert(post)
    elif label == 'RAM': mongodb.RAM.insert(post)
    elif label == 'Case': mongodb.Case.insert(post)
    elif label == 'PSU': mongodb.PSU.insert(post)
    elif label == 'Barebones': mongodb.Barebones.insert(post)
    elif label == 'Storage-HDD': mongodb.HDD.insert(post)
    elif label == 'Storage-SSD': mongodb.SSD.insert(post)
    else: mongodb.MISC.insert(post)


behuizing = ['Behuizingen']
geheugen = ["Geheugen"]
grafische_kaarten = ['Grafische kaarten']
opslag = ['Harde schijven intern']
koeling = ['Koeling']
moederborden = ['Moederborden']
processors = ['Processoren']

behuizing_L3 = ['Desktop']
geheugen_L3 = ['DDR4', 'DDR3', 'DDR2', 'DDR']
grafische_kaarten_L3 = ["PCIe kaarten Matrox", "AGP kaarten", "PCI kaarten"]
opslag_L3 = ["SATA"]
koeling_L3 = ["CPU"]
moederborden_L3 = ["AMD", "Intel"]
processors_L3 = ["Desktop"]

processors_L4 = ["Alles bekijken"]


url = "http://www.alternate.nl"
hardware = "http://www.alternate.nl/html/highlights/page.html?tk=7&lk=7&hgid=189&tgid=906"

behuizing_output = get_subLevel2_url(hardware, url, behuizing)
behuizing_sublinks = get_subLevel3_url(behuizing_output, url, behuizing_L3)
all_behuizing = get_all_product_links(behuizing_sublinks, url)

grafische_kaarten_output = get_subLevel2_url(hardware, url, grafische_kaarten)
grafische_kaarten_sublinks = get_subLevel3_url(grafische_kaarten_output, url, grafische_kaarten_L3)
all_grafische_kaarten = get_all_product_links(grafische_kaarten_sublinks, url)

geheugen_output = get_subLevel2_url(hardware, url, geheugen)
geheugen_sublinks = get_subLevel3_url(geheugen_output, url, geheugen_L3)
all_geheugen = get_all_product_links(geheugen_sublinks, url)

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


# get_RAM(all_geheugen)
get_CPU(all_processors)
# get_Motherboard(all_moederborden)
# get_CPU_Fan(all_koeling)
# get_Case(all_behuizing)
# get_Storage(all_opslag)
# get_GPU(all_grafische_kaarten)


print(len(all_behuizing) + len(all_grafische_kaarten) +
      len(all_koeling) + len(all_moederborden) + len(all_opslag) +
      len(all_processors))
