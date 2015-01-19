__author__ = 'gokhankacan'
from py2neo import neo4j, Node, Relationship, Graph


def func():
    db = Graph("http://localhost:7474/db/data/")

    component = 'CPU'
    # CPU where Core = 4
    """
    print(db.cypher.execute('MATCH(n:{}) WHERE n.AantalCores = "1" RETURN n'.format(component)))
    print(db.cypher.execute('MATCH(n:{}) WHERE n.AantalCores = "2" RETURN n'.format(component)))
    print(db.cypher.execute('MATCH(n:{}) WHERE n.AantalCores = "4" RETURN n'.format(component)))
    print(db.cypher.execute('MATCH(n:{}) WHERE n.AantalCores = "6" RETURN n'.format(component)))
    print(db.cypher.execute('MATCH(n:{}) WHERE n.AantalCores = "8" RETURN n'.format(component)))
    print(db.cypher.execute('MATCH(n:{}) WHERE n.AantalCores = "1" RETURN n'.format(component)))
    """
    n = Node('Component', 'CPU', Name='NULL', Versie='NULL')
    b = Node('Component', 'CPU', Jaar='2015', Opdracht='Neo')


    # db.create(n)
    # print(db.cypher.execute('MATCH (n:CPU) RETURN n'))

    # merge = Node('Component', 'CPU', Name='NULL', Versie='NULL').set("Employee", employee_id=1234)

    node = db.cypher.execute('MERGE(Floris {name: "Laurence Fishburne"})')



    db.create(node)


    # Motherboard
    # CPU
    # CPUFan
    # GraphicsCard
    # RAM
    # Case
    # Storage

func()