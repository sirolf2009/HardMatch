__author__ = 'gokhankacan'
import flask, flask.views
from py2neo import neo4j, Node, Relationship, Graph
from pymongo import Connection


app = flask.Flask(__name__)
app.secret_key = "FrEaKi"
conn = Connection()


@app.route('/')
def homepage():

    title = "Controle Panel HardMatch"
    pageType = 'Homepage'
    db = Graph("http://localhost:7484/db/data/")
    # data = db.cypher.execute_one('MATCH(n:{}) WHERE n.AantalCores = "4" RETURN n'.format('CPU'))


    try:
        return flask.render_template('index.html', title=title, pageType=pageType)
    except Exception as e:
        return str("Exception is been handled at Homepage: ", e)



@app.route('/crawlerCoolblue/')
def coolblue():

    title = "CoolBlue Crawler"
    pageType = 'Crawler'


    try:
        return flask.render_template('coolblue2.html', title=title, pageType=pageType)
    except Exception as e:
        return str("Exception is been handled at Coolblue: ", e)



@app.route('/priceCoolblue/')
def priceHistoryCoolblue():

    title = "Price History"
    pageType = "Coolblue"
    Data = [234, 543, 675, 34, 564, 5436, 343, 233, 45, 565, 3434, 43]



    # Check if Database exists IF not create
    db = conn.coolblue
    cpu = db.cpu

    # cpu.insert({'Name': 'Intel i7', 'Price': '339.99'})
    # cpu.insert({'Name': 'AMD Black Edition', 'Price': '26.99', 'Stock': 'Op voorraad'})
    # cpu.insert({'Name': 'Intel i3', 'Price': '233.99', 'Stock': 'Op voorraad'})



    try:
        return flask.render_template('pricHistory.html', title=title, pageType=pageType, Data=Data)
    except Exception as e:
        return str("Exception is been handled at Price-History Coolblue: ", e)


@app.route('/priceInformatique/')
def priceHistoryInformatique():

    title = "Price History"
    pageType = "Informatique"
    Data = [345, 456, 978, 232, 67, 45, 879, 34, 45, 678, 678, 345]


    try:
        return flask.render_template('pricHistory.html', title=title, pageType=pageType, Data=Data)
    except Exception as e:
        return str("Exception is been handled at Price-History Informatique: ", e)




@app.route('/priceAlternate/')
def priceHistoryAlternate():

    title = "Price History"
    pageType = "Alternate"
    Data = [34534, 5345, 345, 345, 3345, 45, 345, 4354, 3456, 654, 34, 6565]
    tijd = ["Jan"]
    Test = 5


    try:
        return flask.render_template('pricHistory.html', title=title, pageType=pageType, Data=Data, Time=tijd, Test=Test)
    except Exception as e:
        return str("Exception is been handled at Price-History Alternate: ", e)



@app.errorhandler(404)
def page_not_found(e):

    title = "Pagina niet bekend"

    try:
        return flask.render_template('404.html', title=title)
    except Exception as e:
        return str(e)


def main():


    app.debug = True
    app.run()


if __name__ == "__main__": main()