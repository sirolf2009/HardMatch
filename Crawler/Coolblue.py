__author__ = 'gokhankacan'
import requests
from bs4 import BeautifulSoup
# from enum import Enum
from py2neo import neo4j,Node,Relationship,Graph


def categorieLevel():
    start = True
    subCategoriesArray = []

    while start:
        url = 'http://www.processorstore.nl/category/212272/pc-componenten.html'
        html_source = requests.get(url)
        plain_text = html_source.text
        soup = BeautifulSoup(plain_text)

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

            html_source = requests.get(categorie_url)
            plain_text = html_source.text
            soup = BeautifulSoup(plain_text)

            subCategoriePages = soup.findAll('li', {'class': 'paging-navigation-last-page'})[0]
            maxPageNumbers = subCategoriePages.text.strip()

            productListingLevel(int(maxPageNumbers), categorie_url)



def productListingLevel(max_pages, URL):
    page = 1


    while page <= max_pages:
        product_url = URL + '?sort=popularity&dir=d&page=' + str(page)
        html_source = requests.get(product_url)
        plain_text = html_source.text
        soup = BeautifulSoup(plain_text)



        for product in soup.findAll('a', {'class': 'product-list-item--title-link'}):
            href = 'http://www.processorstore.nl' + product.get('href')
            title = product.get('title')

            productPageLevel(title, href)

        page += 1
"""


        for price in soup.findAll('strong', {'class':'product-list-item--price'}):
            price = price.text
            price = price[2:]
            price = price.replace(',', '.')
            print(price)



        for availability in soup.findAll('div', {'class':'product-list-item--assortment-state'}):
            stock = availability.string
            stock = stock.strip()

        print(href)
        print(title)
        print(price)
        print(stock)
        # productPageLevel(title, href, price, stock)
"""


def productPageLevel(title, href):

    # print(title, href, price, stock)
    print(title, href)

    product = href
    html_source = requests.get(product)
    plain_text = html_source.text
    soup = BeautifulSoup(plain_text)


    # Product specification table
    specs_table = soup.findChildren('div', {'class': 'product-specifications is-collapsable is-collapsed'})
    specs_div = soup.findChildren('div', {'class': 'product-specs'})
    specs_dl = soup.findAll('dl', {'class': 'product-specs--list'})

    if specs_table:
        htmlOld(specs_table)
    elif specs_dl:
        htmlNew(specs_dl)
    elif specs_div:
        print('DIV specifications')
    else:
        print("Ik print ELSE")


#TODO in Class verwerken

def htmlNew(sourceCode):

    print(sourceCode)
    print("###############################")
    # TODO: Check alle tabellen <TR>

def htmlOld(sourceCode):
    # wanneer gaat om Tables
    print(sourceCode)
    print("*******************************")
    # TODO: Check alle tabellen <DL>
    for tech in sourceCode.
    product-specs--item-title
    product-specs--item-spec





categorieLevel()
# productPageLevel()