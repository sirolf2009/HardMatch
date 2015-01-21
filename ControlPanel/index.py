__author__ = 'gokhankacan'
import flask, flask.views
from py2neo import neo4j, Node, Relationship, Graph
from pymongo import Connection, MongoClient


app = flask.Flask(__name__)
app.secret_key = "FrEaKi"

client = MongoClient('localhost', 27017)
db = client.coolblue

ddd = [[1147651200000, 67.79], [1147737600000, 64.98], [1147824000000, 65.26], [1147910400000, 63.18], [1147996800000, 64.51], [1148256000000, 63.38], [1148342400000, 63.15], [1148428800000, 63.34], [1148515200000, 64.33], [1148601600000, 63.55], [1148947200000, 61.22], [1149033600000, 59.77]]


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

    cpu = db.CPU.distinct( 'Name' )

    # cpu.insert({'Name': 'Intel i7', 'Price': '339.99'})
    # cpu.insert({'Name': 'AMD Black Edition', 'Price': '26.99', 'Stock': 'Op voorraad'})
    # cpu.insert({'Name': 'Intel i3', 'Price': '233.99', 'Stock': 'Op voorraad'})



    try:
        return flask.render_template('pricHistory.html', title=title, pageType=pageType)
    except Exception as e:
        return str("Exception is been handled at Price-History Coolblue: ", e)


@app.route('/priceInformatique/')
def priceHistoryInformatique():

    title = "Price History"
    pageType = "Informatique"


    try:
        return flask.render_template('pricHistory.html', title=title, pageType=pageType, data=ddd)
    except Exception as e:
        return str("Exception is been handled at Price-History Informatique: ", e)




@app.route('/priceAlternate/')
def priceHistoryAlternate():

    title = "Price History"
    pageType = "Alternate"



    try:
        return flask.render_template('pricHistory.html', title=title, pageType=pageType, data=ddd)
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