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

        product_url = index
        if product_url == "http://www.processorstore.nl/category/212284/upgrade-kits.html":
            break
        else:

            html_source = requests.get(product_url)
            plain_text = html_source.text
            soup = BeautifulSoup(plain_text)

            product = soup.findAll('li', {'class': 'paging-navigation-last-page'})[0]
            maxPageNumbers = product.text.strip()

            productListingLevel(int(maxPageNumbers), product_url)



def productListingLevel(max_pages, URL):
    page = 1

    while page <= max_pages:
        product_url = URL + '?sort=popularity&dir=d&page=' + str(page)
        html_source = requests.get(product_url)
        plain_text = html_source.text
        soup = BeautifulSoup(plain_text)

        for product in soup.findAll('a', {'class': 'product-list-item--title-link'}):

            href = 'http://www.processorstore.nl' + product.get('href')

            productPageLevel(href)
        page += 1



def productPageLevel(url):

    product = url
    html_source = requests.get(product)
    plain_text = html_source.text
    soup = BeautifulSoup(plain_text)

    # Product Image
    product_image = 'No Picture';
    for attributes in soup.findAll('img', {'itemprop': 'image'}):
        # image = soup.findAll('img', {'itemprop': 'image'})
        product_image = attributes.get('src')

    # Product Price
    product_price = soup.findAll('strong', {'itemprop': 'price'})[0]
    price = product_price.text
    price2 = price.strip()


    print(price2[2:])
    print(product_image)


"""
            product = soup.findAll('li', {'class': 'paging-navigation-last-page'})[0]
            maxPageNumbers = product.text.strip()



    for product_Image in soup.findAll('img', {'itemprop': 'image'}):

        productImage = product_Image.get('src')
        print(productImage)

    for product_Price in soup.findAll('strong', {'itemprop': 'price'}):

        productPrice = product_Price.text
        print(productPrice)
"""



#categorieLevel()
productPageLevel('http://www.processorstore.nl/product/513475/intel-core-i7-5930k.html')