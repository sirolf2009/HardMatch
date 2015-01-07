__author__ = 'gokhankacan'
import requests
from bs4 import BeautifulSoup
from py2neo import neo4j,Node,Relationship,Graph



def main():
    # categorieLevel('coolblue')
    pr()


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


def categorieLevel(storeURL):
    start = True
    subCategoriesArray = []

    while start:


        soup = soup_function(stores(storeURL))


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



def productPageLevel(title, href):

    s = soup_function(href)
    print(s.find_parent('tr'))
    # block = s.find('table', {'class':'table table_spectable roundedcorners'})




def pr():
    link = 'http://www.processorstore.nl/product/476816/category-212276/intel-core-i7-4790k.html'

    source = requests.get(link)
    plain = source.text
    soup = BeautifulSoup(plain)


    dl = soup.findChildren('dl', {'class': 'product-specs--list'})

    for i in range(0, len(dl)):

        # print(i)
        # print('###################################')
        # print(dl[i])


        sourceDT = dl[i].text
        soupDT = BeautifulSoup(sourceDT)
        # print(soupDT.find('dt'))






"""
if (soup.findAll('div', {'class': 'product-specifications is-collapsable is-collapsed'})):
    print('Dit TRUE TRUE')

elif (soup.findChildren('dl', {'class': 'product-specs--list'})):


    for dt in soup.findAll('dt', {'class': 'product-specs--item-title'}):

        print(dt.string)

    for dd in soup.findAll('dd', {'class': 'product-specs--item-spec'}):
        print(dd.string)

<<<<<<< Updated upstream
def htmlOld(sourceCode):
    # wanneer gaat om Tables
    print(sourceCode)
    print("*******************************")
    # TODO: Check alle tabellen <DL>
    #for tech in sourceCode.product-specs--item-title #product-specs--item-spec
=======

"""




class productObj():

    def __init__(self, productLink):
        self.specKey = ()
        self.productLink = productLink


if __name__ == '__main__':
    main()