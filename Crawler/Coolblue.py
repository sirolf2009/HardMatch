__author__ = 'gokhankacan'
import requests
from bs4 import BeautifulSoup
# from enum import Enum
from py2neo import neo4j,Node,Relationship,Graph

def stores(store):

    if store == 'informatique':
        link = 'www.informatique.nl'
    elif store == 'alternate':
        link = 'www.alernate.nl'
    elif store == 'azerty':
        link = 'www.azerty.nl'
    elif store == 'coolblue':
        link = 'http://www.processorstore.nl/category/212272/pc-componenten.html'
    elif store == 'mediamarkt':
        link = 'www.mediamarkt.nl'
    else:
        link = 'Geen juiste winkel gekozen'

    return link



def soup_function(args):

    source = requests.get(args)
    plain = source.text
    soup = BeautifulSoup(plain)

    return soup









def categorieLevel():
    start = True
    subCategoriesArray = []

    while start:

        s = stores('coolblue')
        soup = soup_function(s)


        for categories in soup.findAll('a', {'class': 'facetAction'}):

            # title = categories.get('title')
            href = 'http://www.processorstore.nl' + categories.get('href')

            subCategoriesArray.append(href)
            start = False

    productListingPages(subCategoriesArray)











def productListingPages(receiveAllSubCategories):

    for index in receiveAllSubCategories:

        categorie_url = index
        if categorie_url == "http://www.processorstore.nl/category/212284/upgrade-kits.html":
            break
        else:

            # Make a soup Object
            soup = soup_function(categorie_url)


            subCategoriePages = soup.findAll('li', {'class': 'paging-navigation-last-page'})[0]
            maxPageNumbers = subCategoriePages.text.strip()

            productListingLevel(int(maxPageNumbers), categorie_url)









def productListingLevel(max_pages, URL):
    page = 1


    while page <= max_pages:

        soup = soup_function(URL + '?sort=popularity&dir=d&page=' + str(page))


        for product in soup.findAll('a', {'class': 'product-list-item--title-link'}):
            href = 'http://www.processorstore.nl' + product.get('href')
            title = product.get('title')

            productPageLevel(title, href)

        page += 1


"""
        # productPageLevel(title, href, price, stock)
"""






def productPageLevel(title, href):

    # print(title, href, price, stock)
    print(title, href)

    soup = soup_function(href)


    """
    if (soup.findAll('div', {'class': 'product-specifications is-collapsable is-collapsed'})):
        print('Dit TRUE TRUE')

    elif (soup.findChildren('dl', {'class': 'product-specs--list'})):


        for dt in soup.findAll('dt', {'class': 'product-specs--item-title'}):

            print(dt.string)

        for dd in soup.findAll('dd', {'class': 'product-specs--item-spec'}):
            print(dd.string)
    """




<<<<<<< Updated upstream
def htmlOld(sourceCode):
    # wanneer gaat om Tables
    print(sourceCode)
    print("*******************************")
    # TODO: Check alle tabellen <DL>
    #for tech in sourceCode.product-specs--item-title #product-specs--item-spec
=======
>>>>>>> Stashed changes





categorieLevel()